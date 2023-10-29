import pandas as pd
from flask import current_app
from typing import List, Optional, Type
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict
from flask_sqlalchemy import Model
import requests
import json

from app.authentication.models import User
from app.home.models import Rating, RentalHouse, Poi, Recommendation
# from app.config import GEOCODING_APIKEY

import datetime
from dataclasses import dataclass
from typing import List, Any

@dataclass
class Rental:
    id: str
    title: str
    facility_type: str
    accommodation_info: str
    room_info: str
    public_facilities: list
    cooking_facilities: list
    interior_facilities: list
    other_needs: list
    price: str
    distance_to_mrt: str
    mall_info: str
    lat:float
    lng:float
    location_info: str
    location_href: str
    img_src: str

    @staticmethod
    def get_reverseGeocoding(coordinates):
        GEOCODING_APIKEY=current_app.config['GEOCODING_APIKEY']
        url = f'https://maps.googleapis.com/maps/api/geocode/json'
        formatted_string = '{},{}'.format(coordinates[0], coordinates[1])
        parameters = {
            'latlng': formatted_string,
            'key': GEOCODING_APIKEY
        }
        response = requests.get(url, params = parameters)
        if response.status_code == 200:
            data = json.loads(response.text)
            if data["status"]=="OK" :
                result=data["results"][0]["formatted_address"]
                return result
            else:
                print("Invalid query")
                return 1
        else:
            print('Request failed with status code:', response.status_code)
            return 1

    def get_location_info(self):
        loc=self.get_reverseGeocoding([self.lat,self.lng])
        self.location_info=str(loc)
        return 


@dataclass
class FormData:
    minprice: int
    maxprice: int
    location: List[float]
    checkin: datetime.date
    checkout: datetime
    p_rating: float
    l_rating: float
    t_rating: float
    a_rating: float
    roomtype: str
    vector: List[Any]
    desired_month: int
    public_facilities: bool
    cooking_facilities: bool
    interior_facilities: bool
    other_needs: str

    @staticmethod
    def get_geocoding(location):
        GEOCODING_APIKEY=current_app.config['GEOCODING_APIKEY']
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        parameters = {
            'address': location,
            'components': 'country:SG',
            'key': GEOCODING_APIKEY
        }
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and data["results"][0]["formatted_address"] != "Singapore":
                geocoding = data["results"][0]["geometry"]["location"]
                return [geocoding["lat"], geocoding["lng"]]
            else:
                print("Invalid query")
                return [1.352083,103.819836]
        else:
            print('Request failed with status code:', response.status_code)
            return [1.352083,103.819836]

    @classmethod
    def from_form(cls, form,desired_month):
        location = cls.get_geocoding(form.location.data)
        return cls(
            minprice=int(form.minprice.data),
            maxprice=int(form.maxprice.data),
            location=location,
            checkin=form.checkin.data,
            checkout=form.checkout.data,
            p_rating=float(form.p_rating.data),
            l_rating=float(form.l_rating.data),
            t_rating=float(form.t_rating.data),
            a_rating=float(form.a_rating.data),
            roomtype=form.roomtype.data,
            vector=[],
            desired_month=desired_month,
            public_facilities=form.public_facilities.data,
            cooking_facilities=form.cooking_facilities.data,
            interior_facilities=form.interior_facilities.data,
            other_needs=form.other_needs.data
        )


    def get_normalized_weights(self):
        total = float(self.p_rating) + float(self.l_rating) + float(self.t_rating) + float(self.a_rating)
        if total == 0:
            return {
                'price': 0.25,
                'room_type': 0.25,
                'distance': 0.25,
                'amenities': 0.25
            }
        return {
            'price': float(self.p_rating) / total,
            'room_type': float(self.t_rating) / total,
            'distance': float(self.l_rating) / total,
            'amenities': float(self.a_rating) / total
        }
    
    def amenities_to_vector(self,amenities_list):
        reference_list = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
        self.vector = [0] * len(reference_list)
        amenity_mapping = {
            'microwave': 'Microwave',
            'pets': 'Pets',
            'backyard': 'Backyard',
            'oven': 'Oven',
            'stoven': 'stove'
        }
        for amenities in amenities_list:
            for amenity in amenities:
                standardized_amenity = amenity_mapping.get(amenity, amenity)
                if standardized_amenity in reference_list:
                    self.vector[reference_list.index(standardized_amenity)] = 1
        return self.vector

    def convert_amenities_to_input(self):

        # 将所有表单中的多选字段合并到一个列表中
        all_selected_amenities = [self.public_facilities , self.cooking_facilities , self.interior_facilities , self.other_needs]
        return self.amenities_to_vector(all_selected_amenities)


class DataManager:
    def __init__(self,app):
        self.db = app.extensions['sqlalchemy'].db
        # self.Model = self.db.Model

    def get_by_id(self, model: Type[Model], id: int) -> Optional[Model]:
        """Get a single object by its ID."""
        try:
            return self.db.session.query(model).filter_by(id=id).first()
        except Exception as e:
            print(f"Error getting {model.__name__} by ID: {e}")
            return None

    def add(self, obj: Model) -> bool:
        """Add an object to the database."""
        try:
            self.db.session.add(obj)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding object: {e}")
            self.db.session.rollback()
            return False

    def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return self.get_by_id(User, user_id)

    def get_rating(self, user_id: int) -> List[Rating]:
        """Get a poi by ID."""
        return self.get_by_id(Rating, user_id)

    def get_poi(self, poi_id: int) -> Optional[Poi]:
        """Get a poi by ID."""
        return self.get_by_id(Poi, poi_id)

    def get_df_by_ids(self, model: Type[DeclarativeMeta], ids: List[int], id_column_name: str) -> pd.DataFrame:
        """Get records by a list of IDs."""
        query = self.db.session.query(model).filter(getattr(model, id_column_name).in_(ids))
        df = pd.read_sql(query.statement, self.db.engine)
        return df

    def get_recommends(self, house_ids: List[int], id_column_name: str = 'id') -> pd.DataFrame:
        """Get rentalhouses by a list of IDs."""
        return self.get_df_by_ids(RentalHouse, house_ids, id_column_name)
    
    
    def get_df_from_columns(self, model: Type[DeclarativeMeta], columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        query = self.db.session.query(*[getattr(model, column) for column in columns])
        df = pd.read_sql(query.statement, self.db.engine)
        return df
    
    def get_houses_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(RentalHouse, columns)
    
    def get_ratings_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(Rating, columns)
    
    def get_pois_df(self, columns: List[str]) -> pd.DataFrame:
        """Get specific columns of all rows in a table."""
        return self.get_df_from_columns(Poi, columns)
    
    def update_object_by_id(self, model: Model, primary_key_name: str, object_id: int, **kwargs) -> bool:
        """Update an object in the database by ID."""
        try:

            obj = self.db.session.query(model).filter(getattr(model, primary_key_name) == object_id).one()
            
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                else:
                    print(f"Warning: {model.__name__} does not have attribute {key}")
            
            self.db.session.commit()
            return True
        except NoResultFound:
            print(f"{model.__name__} with {primary_key_name} {object_id} not found.")
            return False
        except Exception as e:
            print(f"Error updating {model.__name__}: {e}")
            self.db.session.rollback()
            return False

    def update_recommends_by_uid(self, user_id: int, updates: Dict[str, str]) -> bool:
        """Update a user's recommendation results in the database by user ID."""
        return self.update_object_by_id(Recommendation, 'userID', user_id, **updates)

    def update_rating_by_uid(self, user_id: int, updates: Dict[str, str]) -> bool:
        """Update a user's rating results in the database by user ID."""
        return self.update_object_by_id(Rating, 'userID', user_id, **updates)
