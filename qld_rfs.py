import pandas as pd
import numpy as np
import requests, json

# Constants
STATE = "Queensland"
QLD_RFS = pd.read_csv("data/qld-rfs.csv")

# Functions
def main():
    street_no, street, locality = get_formatted_input()
    geocoding_request_url = make_api_request(street_no, street, locality)
    lat, long = extract_lat_long(geocoding_request_url)
    closest_rfs = find_closest_location(lat, long, QLD_RFS)
    closest_rfs_formatted = f"{closest_rfs["STATION"]}, {closest_rfs["ADDRESS"]}, {closest_rfs["LOCALITY"]}"
    
    print(closest_rfs_formatted)

def get_formatted_input():
    street_no = int(input("Enter your street number "))
    street = input("Enter your street ")
    locality = input("Enter your locality ")  

    return street_no, street, locality

def make_api_request(street_no, street, locality):
    street = street.replace(" ", "+")
    locality = locality.replace(" ", "+")

    geocoding_request_url = f'https://photon.komoot.io/api/?q={street_no}+{street}+{locality}+{STATE}&limit=1'
    return geocoding_request_url

def extract_lat_long(geocoding_request_url):
    geocoding_response = requests.get(geocoding_request_url).json()
    coordinates = geocoding_response['features'][0]['geometry']['coordinates']
    lat = coordinates[1]
    long = coordinates[0] 
    return lat,long

def haversine_vectorized(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c
    return distance

def find_closest_location(reference_lat, reference_lon, locations_df):
    latitudes = locations_df["LAT_GDA20"].values
    longitudes = locations_df["LONG_GDA20"].values
    
    distances = haversine_vectorized(reference_lat, reference_lon, latitudes, longitudes)
    
    closest_location_idx = np.argmin(distances)
    closest_location = locations_df.iloc[closest_location_idx]
    
    return closest_location
    
if __name__ == "__main__":
    main()