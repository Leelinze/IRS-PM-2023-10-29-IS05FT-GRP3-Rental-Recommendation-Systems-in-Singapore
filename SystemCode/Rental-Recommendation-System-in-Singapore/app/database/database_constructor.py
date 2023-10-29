from flask import Flask
# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import pandas as pd
import os
# from models import db,Rating,RentalHouse,User,Poi

current_directory = os.path.dirname(os.path.abspath(__file__))
house_file_path= './final_data.csv'
user_file_path='./userInfo_hashed.csv'
poi_file_path='./poiInfo.csv'
rating_file_path='./ratingInfo.csv'
house_path = os.path.join(current_directory, house_file_path)
user_path=os.path.join(current_directory, user_file_path)
poi_path = os.path.join(current_directory, poi_file_path)
rating_path=os.path.join(current_directory, rating_file_path)
database_file_path = os.path.join(current_directory, 'database.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file_path
db = SQLAlchemy(app)

class RentalHouse(db.Model):
    # __tablename__ = 'RentalHouse'
    HouseID = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    HouseName = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=False)
    neighbourhood_cleansed = db.Column(db.Text, nullable=False)
    neighbourhood_group_cleansed = db.Column(db.Text, nullable=False)
    picture_url = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.Text, nullable=False)
    accommodates= db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_months = db.Column(db.Integer, nullable=False)
    maximum_months = db.Column(db.Integer, nullable=False)
    distance_to_mrt = db.Column(db.Float, nullable=False)
    closest_mrt_name = db.Column(db.Text, nullable=False)
    closest_mrt_stop_id = db.Column(db.Text, nullable=False)
    closest_mall_distance = db.Column(db.Float, nullable=False)
    closest_mall_name = db.Column(db.Text, nullable=False)
    closest_mall_address = db.Column(db.Text, nullable=False)
    aircon = db.Column(db.Boolean, nullable=False)
    BBQ = db.Column(db.Boolean, nullable=False)
    gym = db.Column(db.Boolean, nullable=False)
    pool = db.Column(db.Boolean, nullable=False)
    dryer = db.Column(db.Boolean, nullable=False)
    Wifi = db.Column(db.Boolean, nullable=False)
    kitchen = db.Column(db.Boolean, nullable=False)
    Backyard = db.Column(db.Boolean, nullable=False)
    TV = db.Column(db.Boolean, nullable=False)
    refrigerator = db.Column(db.Boolean, nullable=False)
    Microwave = db.Column(db.Boolean, nullable=False)
    Oven = db.Column(db.Boolean, nullable=False)
    Pets = db.Column(db.Boolean, nullable=False)
    stove = db.Column(db.Boolean, nullable=False)
    fan = db.Column(db.Boolean, nullable=False)
    accommodates=db.Column(db.Integer, nullable=False)
    listing_url = db.Column(db.Text, nullable=False)
    review_scores_rating=db.Column(db.Float, nullable=False)
    review_scores_accuracy=db.Column(db.Float, nullable=False)
    review_scores_cleanliness=db.Column(db.Float, nullable=False)
    review_scores_checkin=db.Column(db.Float, nullable=False)
    review_scores_communication=db.Column(db.Float, nullable=False)
    review_scores_location=db.Column(db.Float, nullable=False)
    review_scores_value=db.Column(db.Float, nullable=False)



class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.userName

    def get_id(self):
        return self.userID

class Rating(db.Model):
    # __tablename__ = 'rating'
    ratingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.Integer)
    listing_id = db.Column(db.Integer)
    rating = db.Column(db.Float)
    comments=db.Column(db.Text)

class Poi(db.Model):
    # __tablename__ = 'poi'
    POIid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name= db.Column(db.String)
    lat= db.Column(db.Float)
    lng= db.Column(db.Float)
    formatted_address= db.Column(db.String)
    store = db.Column(db.Boolean, nullable=False)
    food = db.Column(db.Boolean, nullable=False)
    health = db.Column(db.Boolean, nullable=False)
    restaurant = db.Column(db.Boolean, nullable=False)
    hospital = db.Column(db.Boolean, nullable=False)
    lodging = db.Column(db.Boolean, nullable=False)
    finance = db.Column(db.Boolean, nullable=False)
    cafe = db.Column(db.Boolean, nullable=False)
    convenience_store = db.Column(db.Boolean, nullable=False)
    clothing_store = db.Column(db.Boolean, nullable=False)
    atm = db.Column(db.Boolean, nullable=False)
    shopping_mall = db.Column(db.Boolean, nullable=False)
    grocery_or_supermarket = db.Column(db.Boolean, nullable=False)
    home_goods_store = db.Column(db.Boolean, nullable=False)
    school = db.Column(db.Boolean, nullable=False)
    bakery = db.Column(db.Boolean, nullable=False)
    beauty_salon = db.Column(db.Boolean, nullable=False)
    transit_station = db.Column(db.Boolean, nullable=False)
    place_of_worship = db.Column(db.Boolean, nullable=False)
    pharmacy = db.Column(db.Boolean, nullable=False)
    meal_takeaway = db.Column(db.Boolean, nullable=False)
    furniture_store = db.Column(db.Boolean, nullable=False)
    tourist_attraction = db.Column(db.Boolean, nullable=False)
    secondary_school = db.Column(db.Boolean, nullable=False)
    supermarket = db.Column(db.Boolean, nullable=False)
    doctor = db.Column(db.Boolean, nullable=False)
    shoe_store = db.Column(db.Boolean, nullable=False)
    dentist = db.Column(db.Boolean, nullable=False)
    jewelry_store = db.Column(db.Boolean, nullable=False)
    church = db.Column(db.Boolean, nullable=False)
    bank = db.Column(db.Boolean, nullable=False)
    primary_school = db.Column(db.Boolean, nullable=False)
    electronics_store = db.Column(db.Boolean, nullable=False)
    gym = db.Column(db.Boolean, nullable=False)
    spa = db.Column(db.Boolean, nullable=False)
    car_repair = db.Column(db.Boolean, nullable=False)
    pet_store = db.Column(db.Boolean, nullable=False)
    bus_station = db.Column(db.Boolean, nullable=False)
    university = db.Column(db.Boolean, nullable=False)
    park = db.Column(db.Boolean, nullable=False)
    general_contractor = db.Column(db.Boolean, nullable=False)
    subway_station = db.Column(db.Boolean, nullable=False)
    real_estate_agency = db.Column(db.Boolean, nullable=False)
    florist = db.Column(db.Boolean, nullable=False)
    hair_care = db.Column(db.Boolean, nullable=False)
    department_store = db.Column(db.Boolean, nullable=False)
    hardware_store = db.Column(db.Boolean, nullable=False)
    car_dealer = db.Column(db.Boolean, nullable=False)
    veterinary_care = db.Column(db.Boolean, nullable=False)
    travel_agency = db.Column(db.Boolean, nullable=False)
    bicycle_store = db.Column(db.Boolean, nullable=False)
    book_store = db.Column(db.Boolean, nullable=False)
    laundry = db.Column(db.Boolean, nullable=False)
    plumber = db.Column(db.Boolean, nullable=False)
    meal_delivery = db.Column(db.Boolean, nullable=False)
    lawyer = db.Column(db.Boolean, nullable=False)
    parking = db.Column(db.Boolean, nullable=False)
    mosque = db.Column(db.Boolean, nullable=False)
    physiotherapist = db.Column(db.Boolean, nullable=False)
    art_gallery = db.Column(db.Boolean, nullable=False)
    insurance_agency = db.Column(db.Boolean, nullable=False)
    bar = db.Column(db.Boolean, nullable=False)
    museum = db.Column(db.Boolean, nullable=False)
    storage = db.Column(db.Boolean, nullable=False)
    movie_theater = db.Column(db.Boolean, nullable=False)
    moving_company = db.Column(db.Boolean, nullable=False)
    liquor_store = db.Column(db.Boolean, nullable=False)
    gas_station = db.Column(db.Boolean, nullable=False)
    electrician = db.Column(db.Boolean, nullable=False)
    car_rental = db.Column(db.Boolean, nullable=False)
    locksmith = db.Column(db.Boolean, nullable=False)
    car_wash = db.Column(db.Boolean, nullable=False)
    post_office = db.Column(db.Boolean, nullable=False)
    embassy = db.Column(db.Boolean, nullable=False)
    night_club = db.Column(db.Boolean, nullable=False)
    fire_station = db.Column(db.Boolean, nullable=False)
    amusement_park = db.Column(db.Boolean, nullable=False)
    library = db.Column(db.Boolean, nullable=False)
    hindu_temple = db.Column(db.Boolean, nullable=False)
    local_government_office = db.Column(db.Boolean, nullable=False)
    funeral_home = db.Column(db.Boolean, nullable=False)
    bowling_alley = db.Column(db.Boolean, nullable=False)
    cemetery = db.Column(db.Boolean, nullable=False)
    aquarium = db.Column(db.Boolean, nullable=False)
    roofing_contractor = db.Column(db.Boolean, nullable=False)
    stadium = db.Column(db.Boolean, nullable=False)
    painter = db.Column(db.Boolean, nullable=False)
    courthouse = db.Column(db.Boolean, nullable=False)
    drugstore = db.Column(db.Boolean, nullable=False)
    campground = db.Column(db.Boolean, nullable=False)
    accounting = db.Column(db.Boolean, nullable=False)
    airport = db.Column(db.Boolean, nullable=False)
    zoo = db.Column(db.Boolean, nullable=False)
    casino = db.Column(db.Boolean, nullable=False)
    synagogue = db.Column(db.Boolean, nullable=False)
    premise = db.Column(db.Boolean, nullable=False)
    taxi_stand = db.Column(db.Boolean, nullable=False)
    police = db.Column(db.Boolean, nullable=False)
    light_rail_station = db.Column(db.Boolean, nullable=False)
    city_hall = db.Column(db.Boolean, nullable=False)
    train_station = db.Column(db.Boolean, nullable=False)
    natural_feature = db.Column(db.Boolean, nullable=False)
    subpremise = db.Column(db.Boolean, nullable=False)

def import_user_data(user_path):
    df = pd.read_csv(user_path)
    for index, row in df.iterrows():
        user = User(
            userID=row.get('userID'),
            userName=row.get('userName'),
            password=row.get('password')
        )
        db.session.add(user)
    db.session.commit()

def import_rental_data(house_path):
    df = pd.read_csv(house_path)
    for index, row in df.iterrows():
        house = RentalHouse(
            HouseID=row['HouseID'],
            HouseName=row['HouseName'],
            details=row['details'],
            neighbourhood_cleansed=row['neighbourhood_cleansed'],
            neighbourhood_group_cleansed=row['neighbourhood_group_cleansed'],
            picture_url=row['picture_url'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            room_type=row['room_type'],
            accommodates=row['accommodates'],
            price=row['price'],
            minimum_months=row['minimum_months'],
            maximum_months=row['maximum_months'],
            distance_to_mrt=row['distance_to_mrt'],
            closest_mrt_name=row['closest_mrt_name'],
            closest_mrt_stop_id=row['closest_mrt_stop_id'],
            closest_mall_distance=row['closest_mall_distance'],
            closest_mall_name=row['closest_mall_name'],
            closest_mall_address=row['closest_mall_address'],
            aircon=row['aircon'],
            BBQ=row['BBQ'],
            gym=row['gym'],
            pool=row['pool'],
            dryer=row['dryer'],
            Wifi=row['Wifi'],
            kitchen=row['kitchen'],
            Backyard=row['Backyard'],
            TV=row['TV'],
            refrigerator=row['refrigerator'],
            Microwave=row['Microwave'],
            Oven=row['Oven'],
            Pets=row['Pets'],
            stove=row['stove'],
            fan=row['fan'],
            listing_url=row['listing_url'],
            review_scores_rating=row['review_scores_rating'],
            review_scores_accuracy=row['review_scores_accuracy'],
            review_scores_cleanliness=row['review_scores_cleanliness'],
            review_scores_checkin=row['review_scores_checkin'],
            review_scores_communication=row['review_scores_communication'],
            review_scores_location=row['review_scores_location'],
            review_scores_value=row['review_scores_value']
        )
        db.session.add(house)
    db.session.commit()

def import_rating_data(rating_path):
    df = pd.read_csv(rating_path)
    for index, row in df.iterrows():
        rating = Rating(
            ratingID=index,
            userID=row.get('userID'),
            listing_id=row.get('listing_id'),
            rating=row.get('rating'),
            comments=row.get('comments', '')
        )
        db.session.add(rating)
    db.session.commit()

def import_poi_data(poi_path):
    df = pd.read_csv(poi_path)
    for index, row in df.iterrows():
        poi = Poi(
            POIid=index,
            name=row['name'],
            formatted_address=row['formatted_address'],
            lat=row['lat'],
            lng=row['lng'],
            store=row.get('store', False),
            food=row.get('food', False),
            health=row.get('health', False),
            restaurant=row.get('restaurant', False),
            hospital=row.get('hospital', False),
            lodging=row.get('lodging', False),
            finance=row.get('finance', False),
            cafe=row.get('cafe', False),
            convenience_store=row.get('convenience_store', False),
            clothing_store=row.get('clothing_store', False),
            atm=row.get('atm', False),
            shopping_mall=row.get('shopping_mall', False),
            grocery_or_supermarket=row.get('grocery_or_supermarket', False),
            home_goods_store=row.get('home_goods_store', False),
            school=row.get('school', False),
            bakery=row.get('bakery', False),
            beauty_salon=row.get('beauty_salon', False),
            transit_station=row.get('transit_station', False),
            place_of_worship=row.get('place_of_worship', False),
            pharmacy=row.get('pharmacy', False),
            meal_takeaway=row.get('meal_takeaway', False),
            furniture_store=row.get('furniture_store', False),
            tourist_attraction=row.get('tourist_attraction', False),
            secondary_school=row.get('secondary_school', False),
            supermarket=row.get('supermarket', False),
            doctor=row.get('doctor', False),
            shoe_store=row.get('shoe_store', False),
            dentist=row.get('dentist', False),
            jewelry_store=row.get('jewelry_store', False),
            church=row.get('church', False),
            bank=row.get('bank', False),
            primary_school=row.get('primary_school', False),
            electronics_store=row.get('electronics_store', False),
            gym=row.get('gym', False),
            spa=row.get('spa', False),
            car_repair=row.get('car_repair', False),
            pet_store=row.get('pet_store', False),
            bus_station=row.get('bus_station', False),
            university=row.get('university', False),
            park=row.get('park', False),
            general_contractor=row.get('general_contractor', False),
            subway_station=row.get('subway_station', False),
            real_estate_agency=row.get('real_estate_agency', False),
            florist=row.get('florist', False),
            hair_care=row.get('hair_care', False),
            department_store=row.get('department_store', False),
            hardware_store=row.get('hardware_store', False),
            car_dealer=row.get('car_dealer', False),
            veterinary_care=row.get('veterinary_care', False),
            travel_agency=row.get('travel_agency', False),
            bicycle_store=row.get('bicycle_store', False),
            book_store=row.get('book_store', False),
            laundry=row.get('laundry', False),
            plumber=row.get('plumber', False),
            meal_delivery=row.get('meal_delivery', False),
            lawyer=row.get('lawyer', False),
            parking=row.get('parking', False),
            mosque=row.get('mosque', False),
            physiotherapist=row.get('physiotherapist', False),
            art_gallery=row.get('art_gallery', False),
            insurance_agency=row.get('insurance_agency', False),
            bar=row.get('bar', False),
            museum=row.get('museum', False),
            storage=row.get('storage', False),
            movie_theater=row.get('movie_theater', False),
            moving_company=row.get('moving_company', False),
            liquor_store=row.get('liquor_store', False),
            gas_station=row.get('gas_station', False),
            electrician=row.get('electrician', False),
            car_rental=row.get('car_rental', False),
            locksmith=row.get('locksmith', False),
            car_wash=row.get('car_wash', False),
            post_office=row.get('post_office', False),
            embassy=row.get('embassy', False),
            night_club=row.get('night_club', False),
            fire_station=row.get('fire_station', False),
            amusement_park=row.get('amusement_park', False),
            library=row.get('library', False),
            hindu_temple=row.get('hindu_temple', False),
            local_government_office=row.get('local_government_office', False),
            funeral_home=row.get('funeral_home', False),
            bowling_alley=row.get('bowling_alley', False),
            cemetery=row.get('cemetery', False),
            aquarium=row.get('aquarium', False),
            roofing_contractor=row.get('roofing_contractor', False),
            stadium=row.get('stadium', False),
            painter=row.get('painter', False),
            courthouse=row.get('courthouse', False),
            drugstore=row.get('drugstore', False),
            campground=row.get('campground', False),
            accounting=row.get('accounting', False),
            airport=row.get('airport', False),
            zoo=row.get('zoo', False),
            casino=row.get('casino', False),
            synagogue=row.get('synagogue', False),
            premise=row.get('premise', False),
            taxi_stand=row.get('taxi_stand', False),
            police=row.get('police', False),
            light_rail_station=row.get('light_rail_station', False),
            city_hall=row.get('city_hall', False),
            train_station=row.get('train_station', False),
            natural_feature=row.get('natural_feature', False),
            subpremise=row.get('subpremise', False),
        )
        db.session.add(poi)
    db.session.commit()

# Read Test Function
def read_test():
    # Example: Read first 5 users
    users = User.query.limit(5).all()
    for user in users:
        print(user.userID, user.userName)

    # Add more read tests as needed

# Insert Test Function
def insert_test():
    # Example: Insert a test user without setting userID
    test_user = User(userName='TestUser', password='TestPassword')
    db.session.add(test_user)
    db.session.commit()

    # Verify if test user is inserted
    inserted_user = User.query.filter_by(userName='TestUser', password='TestPassword').first()
    if inserted_user:
        print(f'Insert Test Passed: User with userName TestUser is inserted with userID {inserted_user.userID}.')
        return True, inserted_user.userID
    else:
        print('Insert Test Failed: User with userName TestUser is not found.')
        return False, None
# Delete Test Data Function
def delete_test_data():
    # Example: Delete the test user
    test_user = User.query.filter_by(userName='TestUser').first()
    if test_user:
        db.session.delete(test_user)
        db.session.commit()
        print('Test data deleted successfully.')
    else:
        print('Test data not found.')



if __name__ == '__main__':
    
    with app.app_context():
        db.drop_all()  
        db.create_all()
        import_user_data(user_path)
        import_poi_data(poi_path)
        import_rating_data(rating_path)
        import_rental_data(house_path)

        # Perform Read Test
        read_test()

        # Perform Insert Test and Delete Test Data if Passed
        if insert_test():
            delete_test_data()