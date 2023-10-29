import numpy as np
import pandas as pd
import re
from dataclasses import asdict
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
# from app.services.DataManger import DataManager
# from app.services.MapDrawer import MapDrawer

from flask import current_app

# from app.services.DataManger import FormData,Rental
from app.services.DataManger import Rental

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2) * np.sin(dlat/2) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2) * np.sin(dlon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d

def form_to_vecs(form_data):

    desired_price_min = form_data.minprice
    desired_price_max = form_data.maxprice
    desired_roomtype = form_data.roomtype
    desired_month = form_data.desired_month
    desired_latitude, desired_longitude = form_data.location
    form_data.convert_amenities_to_input()
    user_amenities_input = form_data.vector
    weights = form_data.get_normalized_weights()
    

    desired_price = (desired_price_min + desired_price_max) / 2


    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    selected_amenities = [amenities_columns[i] for i, val in enumerate(user_amenities_input) if val == 1]
    roomtype_col = "room_type_" + desired_roomtype
    data_cols = ['HouseID'] + selected_amenities + ['latitude', 'longitude', 'room_type', 'price', 'minimum_months', 'maximum_months']


    data = current_app.data_manager.get_houses_df(data_cols)
    data = data.replace({True: 1, False: 0})


    filtered_data = data[(data['maximum_months'] >= desired_month) & (data['minimum_months'] <= desired_month)]


    encoder = OneHotEncoder(sparse=False)
    onehot = encoder.fit_transform(filtered_data[['room_type']])
    onehot_df = pd.DataFrame(onehot, columns=encoder.get_feature_names_out(['room_type']))
    filtered_data = pd.concat([filtered_data.reset_index(drop=True), onehot_df.reset_index(drop=True)], axis=1)


    price_scaler = RobustScaler()
    distance_scaler = RobustScaler()

    weight_distance = 2
    inverse_weight_distance=1/(weight_distance + 1e-5)  # 加一个小的常数防止除以0
    filtered_data['distance'] = haversine_distance(desired_latitude, desired_longitude, filtered_data['latitude'], filtered_data['longitude'])
    filtered_data['inverse_distance'] = 1 / (filtered_data['distance'] + 1e-5)
    filtered_data['similarity_distance'] = distance_scaler.fit_transform(filtered_data['inverse_distance'].values.reshape(-1, 1))
    similarity_weight_distance=distance_scaler.transform(np.array(inverse_weight_distance).reshape(-1, 1))[0, 0]
    

    # max_base_pricediff = desired_price_max - desired_price_min  
    max_base_pricediff=200
    weight_pricediff = max_base_pricediff * (1 - weights['price'])
    inverse_weight_pricediff=1/weight_pricediff  
    
    filtered_data['price_difference'] = abs(filtered_data['price'] - desired_price)
    filtered_data['reciprocal_price_difference'] = 1 / (filtered_data['price_difference'] + 1e-5)
    filtered_data['normalized_reciprocal_price_difference'] = price_scaler.fit_transform(filtered_data['reciprocal_price_difference'].values.reshape(-1, 1))
    similarity_weight_pricediff=price_scaler.transform(np.array(inverse_weight_pricediff).reshape(-1, 1))[0, 0]

    amenities_weights = [weights['amenities'] / len(selected_amenities)] * len(selected_amenities)
    room_type_weight_per_feature = weights['room_type'] / len([roomtype_col])
    weight_vector = amenities_weights  + [weights['distance']] + [room_type_weight_per_feature] + [weights['price']]

    user_room_type = [1 if roomtype == roomtype_col else -1 for roomtype in [roomtype_col]]
    user_vector_w = np.array([1] * len(selected_amenities) + [similarity_weight_distance] + user_room_type + [similarity_weight_pricediff])

    vector_cols = selected_amenities + ['similarity_distance'] + [roomtype_col] + ['normalized_reciprocal_price_difference', 'HouseID']
    data_vector = filtered_data[vector_cols]

    return weight_vector, user_vector_w, data_vector

def df_to_am(df):
    categories = {
        'public_facilities': ['BBQ', 'gym', 'pool', 'Backyard'],
        'cooking_facilities': ['kitchen', 'refrigerator', 'Microwave', 'Oven', 'stove'],
        'interior_facilities': ['conditioning', 'dryer', 'Wifi', 'TV', 'fan'],
        'other_needs': ['Pets']
    }

    result_dict = {category: [] for category in categories}

    for index, row in df.iterrows():
        for category, facilities in categories.items():
            for facility in facilities:
                if row[facility] == 1:
                    result_dict[category].append(facility)
    return result_dict


def vector_to_amenities(vector):
    categories = [
        ['aircon', 'BBQ', 'gym'],  
        ['pool', 'dryer', 'Wifi'],  
        ['kitchen', 'Backyard', 'TV', 'refrigerator'], 
        ['Microwave', 'Oven', 'Pets', 'stove', 'fan'] 
    ]
    
    amenities_list = [[] for _ in range(4)]
    flat_categories = [item for sublist in categories for item in sublist]
    
    for i, value in enumerate(vector):
        if value == 1:
            for j, category in enumerate(categories):
                if flat_categories[i] in category:
                    amenities_list[j].append(flat_categories[i])
                    break
                
    return amenities_list


def df_to_amenities(raw):
    amenities_columns = ['aircon', 'BBQ', 'gym', 'pool', 'dryer', 'Wifi', 'kitchen', 'Backyard', 'TV', 'refrigerator', 'Microwave', 'Oven', 'Pets', 'stove', 'fan']
    amenities_values = [getattr(raw, col) for col in amenities_columns]
    amenities_list = vector_to_amenities(amenities_values)
    return amenities_list

def df_to_display(row_num,raw):
    amenities_list=df_to_amenities(raw)
    room_info = str(getattr(raw, 'details'))
    cleaned_room_info = re.sub(r'\?\?+', '. ', room_info)
    rental=Rental(
        id=str(getattr(raw, 'HouseID')),
        title=str(getattr(raw, 'HouseName')),
        facility_type=str(getattr(raw, 'room_type')),
        accommodation_info=str(getattr(raw, 'accommodates'))+" accommodate",
        room_info=cleaned_room_info,
        public_facilities=amenities_list[0],
        cooking_facilities=amenities_list[1],
        interior_facilities=amenities_list[2],
        other_needs=amenities_list[3],
        price="S$ "+ str(getattr(raw, 'price'))+ "/month",
        distance_to_mrt=str(int(getattr(raw, 'distance_to_mrt')*1000)) + "m to " + str(getattr(raw, 'closest_mrt_name')),
        mall_info=str(int(getattr(raw, 'closest_mall_distance')*1000)) + "m to " + str(getattr(raw, 'closest_mall_name')) + "(" + str(getattr(raw, 'closest_mall_address')) + ")",
        lat=str(getattr(raw, 'latitude')),
        lng=str(getattr(raw, 'longitude')),
        location_info=None,
        location_href="./map/" + str((row_num)),
        img_src=str(getattr(raw, 'picture_url'))
    )
    rental.get_location_info()
    rental_dic=asdict(rental)
    return rental_dic

def get_ratings():
    rating_cols=['userID', 'listing_id', 'rating']
    rating_info = current_app.data_manager.get_ratings_df(rating_cols)
    rating_info.columns = ['user_id','item_id','rating']
    rating_info = rating_info.drop(rating_info[rating_info.rating == 0].index)
    return rating_info

