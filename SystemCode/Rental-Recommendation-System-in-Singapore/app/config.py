import os, random, string
from dotenv import load_dotenv


# basedir = os.path.abspath(os.path.dirname(__file__))

# GEOCODING_APIKEY = os.getenv('GEOCODING_APIKEY', None)


class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    dotenv_path = os.path.join(basedir, '.env')
    load_dotenv(dotenv_path)
    print(dotenv_path)
    print(os.listdir(basedir))  
    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))     

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 

    # try to set up a Relational DBMS
    if DB_ENGINE and DB_NAME and DB_USERNAME:

        try:
            
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            ) 

            USE_SQLITE  = False

        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')    

    if USE_SQLITE:

        # This will create a file in <app> FOLDER
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'database.db')

    GEOCODING_APIKEY = os.getenv('GEOCODING_APIKEY', None)
    
    GEOJSON_FILE_PATH = os.path.join(basedir,'database', "neighbourhoods.geojson")

    RF_MODEL_PATH=os.path.join(basedir,'models', "RatingEstimation_random_forest_model.joblib")

    MF_MODEL_PATH=os.path.join(basedir,'models', "SVD_matrix_factorization_model.surprise")

    SVD_PARAM={
        'n_factors': 100, 
        'n_epochs': 50, 
        'lr_all': 0.007, 
        'reg_all': 0.02, 
        'lr_bu': 0.005, 
        'lr_bi': 0.005, 
        'reg_bu': 0.02, 
        'reg_bi': 0.01, 
        'lr_pu': 0.01, 
        'lr_qi': 0.01, 
        'reg_pu': 0.01, 
        'reg_qi': 0.02
    } 

    RECOMMEND_DEFAULT_TOPN=10

    ALPHA=0.7
    POI_COLUMNS = ['store', 'food', 'health', 'restaurant', 'hospital', 'lodging', 'finance', 'cafe', 'convenience_store', 
               'clothing_store', 'atm', 'shopping_mall', 'grocery_or_supermarket', 'home_goods_store', 'school', 
               'bakery', 'beauty_salon', 'transit_station', 'place_of_worship', 'pharmacy', 'meal_takeaway', 
               'furniture_store', 'tourist_attraction', 'secondary_school', 'supermarket', 'doctor', 'shoe_store', 
               'dentist', 'jewelry_store', 'church', 'bank', 'primary_school', 'electronics_store', 'gym', 'spa', 
               'car_repair', 'pet_store', 'bus_station', 'university', 'park', 'general_contractor', 'subway_station', 
               'real_estate_agency', 'florist', 'hair_care', 'department_store', 'hardware_store', 'car_dealer', 
               'veterinary_care', 'travel_agency', 'bicycle_store', 'book_store', 'laundry', 'plumber', 
               'meal_delivery', 'lawyer', 'parking', 'mosque', 'physiotherapist', 'art_gallery', 'insurance_agency', 
               'bar', 'museum', 'storage', 'movie_theater', 'moving_company', 'liquor_store', 'gas_station', 
               'electrician', 'car_rental', 'locksmith', 'car_wash', 'post_office', 'embassy', 'night_club', 
               'fire_station', 'amusement_park', 'library', 'hindu_temple', 'local_government_office', 
               'funeral_home', 'bowling_alley', 'cemetery', 'aquarium', 'roofing_contractor', 'stadium', 'painter', 
               'courthouse', 'drugstore', 'campground', 'accounting', 'airport', 'zoo', 'casino', 'synagogue', 
               'premise', 'taxi_stand', 'police', 'light_rail_station', 'city_hall', 'train_station', 
               'natural_feature', 'subpremise']
    SEMANTIC_GROUPS = {
        'store_group': ['store', 'shopping_mall', 'grocery_or_supermarket', 'convenience_store', 'clothing_store', 'home_goods_store', 'electronics_store', 'department_store', 'furniture_store'],
        'food_group': ['food', 'restaurant', 'cafe', 'bakery', 'meal_takeaway'],
        'health_group': ['health', 'hospital', 'pharmacy', 'doctor', 'dentist', 'physiotherapist'],
        'finance_group': ['finance', 'atm', 'bank', 'insurance_agency'],
        'education_group': ['school', 'secondary_school', 'primary_school', 'university'],
        'transportation_group': ['transit_station', 'bus_station', 'subway_station', 'taxi_stand', 'train_station', 'light_rail_station'],
        'entertainment_group': ['movie_theater', 'amusement_park', 'bowling_alley', 'casino', 'night_club'],
        'culture_group': ['museum', 'art_gallery', 'library', 'hindu_temple', 'church', 'mosque', 'synagogue'],
        'recreation_group': ['park', 'gym', 'spa', 'stadium', 'zoo', 'aquarium'],
        'services_group': ['laundry', 'plumber', 'lawyer', 'post_office', 'car_wash', 'embassy', 'police', 'funeral_home', 'moving_company']
    }

    COLORS = ['#8B0000', '#DC143C', '#FF7F50', '#CD5C5C', '#FA8072', '#FF8C00', '#FFD700', '#A52A2A', '#FF6347', '#FFA07A']
    MAP_CENTER=[1.3521, 103.8198] #center of Singapore


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}



    