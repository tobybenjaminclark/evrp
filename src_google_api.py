
from enum import Enum
from keys import GOOGLE_API_KEY
import requests

class PlaceType(Enum):
    ACCOUNTING = "accounting"
    AIRPORT = "airport"
    AMUSEMENT_PARK = "amusement_park"
    AQUARIUM = "aquarium"
    ART_GALLERY = "art_gallery"
    ATM = "atm"
    BAKERY = "bakery"
    BANK = "bank"
    BAR = "bar"
    BEAUTY_SALON = "beauty_salon"
    BICYCLE_STORE = "bicycle_store"
    BOOK_STORE = "book_store"
    BOWLING_ALLEY = "bowling_alley"
    BUS_STATION = "bus_station"
    CAFE = "cafe"
    CAMPGROUND = "campground"
    CAR_DEALER = "car_dealer"
    CAR_RENTAL = "car_rental"
    CAR_REPAIR = "car_repair"
    CAR_WASH = "car_wash"
    CASINO = "casino"
    CEMETERY = "cemetery"
    CHURCH = "church"
    CITY_HALL = "city_hall"
    CLOTHING_STORE = "clothing_store"
    CONVENIENCE_STORE = "convenience_store"
    COURTHOUSE = "courthouse"
    DENTIST = "dentist"
    DEPARTMENT_STORE = "department_store"
    DOCTOR = "doctor"
    DRUGSTORE = "drugstore"
    ELECTRICIAN = "electrician"
    ELECTRONICS_STORE = "electronics_store"
    EMBASSY = "embassy"
    FIRE_STATION = "fire_station"
    FLORIST = "florist"
    FUNERAL_HOME = "funeral_home"
    FURNITURE_STORE = "furniture_store"
    GAS_STATION = "gas_station"
    GYM = "gym"
    HAIR_CARE = "hair_care"
    HARDWARE_STORE = "hardware_store"
    HINDU_TEMPLE = "hindu_temple"
    HOME_GOODS_STORE = "home_goods_store"
    HOSPITAL = "hospital"
    INSURANCE_AGENCY = "insurance_agency"
    JEWELRY_STORE = "jewelry_store"
    LAUNDRY = "laundry"
    LAWYER = "lawyer"
    LIBRARY = "library"
    LIGHT_RAIL_STATION = "light_rail_station"
    LIQUOR_STORE = "liquor_store"
    LOCAL_GOVERNMENT_OFFICE = "local_government_office"
    LOCKSMITH = "locksmith"
    LODGING = "lodging"
    MEAL_DELIVERY = "meal_delivery"
    MEAL_TAKEAWAY = "meal_takeaway"
    MOSQUE = "mosque"
    MOVIE_RENTAL = "movie_rental"
    MOVIE_THEATER = "movie_theater"
    MOVING_COMPANY = "moving_company"
    MUSEUM = "museum"
    NIGHT_CLUB = "night_club"
    PAINTER = "painter"
    PARK = "park"
    PARKING = "parking"
    PET_STORE = "pet_store"
    PHARMACY = "pharmacy"
    PHYSIOTHERAPIST = "physiotherapist"
    PLUMBER = "plumber"
    POLICE = "police"
    POST_OFFICE = "post_office"
    PRIMARY_SCHOOL = "primary_school"
    REAL_ESTATE_AGENCY = "real_estate_agency"
    RESTAURANT = "restaurant"
    ROOFING_CONTRACTOR = "roofing_contractor"
    RV_PARK = "rv_park"
    SCHOOL = "school"
    SECONDARY_SCHOOL = "secondary_school"
    SHOE_STORE = "shoe_store"
    SHOPPING_MALL = "shopping_mall"
    SPA = "spa"
    STADIUM = "stadium"
    STORAGE = "storage"
    STORE = "store"
    SUBWAY_STATION = "subway_station"
    SUPERMARKET = "supermarket"
    SYNAGOGUE = "synagogue"
    TAXI_STAND = "taxi_stand"
    TOURIST_ATTRACTION = "tourist_attraction"
    TRAIN_STATION = "train_station"
    TRANSIT_STATION = "transit_station"
    TRAVEL_AGENCY = "travel_agency"
    UNIVERSITY = "university"
    VETERINARY_CARE = "veterinary_care"
    ZOO = "zoo"
    NONE = "None"


def google_nearby_search(location: tuple[float, float], radius: int, keyword = "", type: PlaceType = PlaceType.NONE) -> dict:

    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'key': GOOGLE_API_KEY,
        'location': f"{location[0]},{location[1]}",
        'radius': radius,
    }

    if type != PlaceType.NONE: params['type'] = type.value
    if keyword != "": params['keyword'] = keyword

    try:
        # Send request to Google Places API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        results = response.json().get('results', [])
        return results

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  # Print error message
        return []             # Return an empty list in case of error


def get_elevation_data(locations_str):
    # Construct the request URL
    request_url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={locations_str}&key={GOOGLE_API_KEY}'


    try:
        # Make the request to the Elevation API
        response = requests.get(request_url)
        # Check if the request was successful
        if response.status_code == 200:
            elevation_data_chunk = response.json().get('results', [])
        else:
            print(f'Elevation API Error (1): {response.status_code}\n{response.text}')
            return None

    except requests.exceptions.RequestException as e:
        print(f'Elevation API Error (2): {e}\nResponse: {response}')
        return None

    return elevation_data_chunk


def get_coordinates_from_keyword(keyword):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": keyword,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            place = data['results'][0]
            location = place['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            return (latitude, longitude)
        else:   raise Exception(f'Error: {response.status_code}\n{response.text}')
    else:       raise Exception(f'Error: {response.status_code}\n{response.text}')
