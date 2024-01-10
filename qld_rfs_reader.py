import pandas as pd
import requests, json

# Constants
STATE = "Queensland"
QLD_RFS = pd.read_csv("data/qld-rfs.csv")

# Functions
def main():
    api_call = get_formatted_api_call()
    lat, long = extract_lat_long(api_call)
    closest_rfs_lat = find_closest_value_pandas(lat, QLD_RFS["LAT_GDA20"])
    closest_rfs_long = find_closest_value_pandas(long, QLD_RFS["LONG_GDA20"])

    closest_rfs = QLD_RFS[QLD_RFS["LAT_GDA20"] == closest_rfs_lat]
    closest_rfs = QLD_RFS[QLD_RFS["LONG_GDA20"] == closest_rfs_long]
    
    print(closest_rfs)

def get_formatted_api_call():
    street_no = float(input("Enter your street number "))
    street = input("Enter your street ")
    locality = input("Enter your locality ")  

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

def find_closest_value_pandas(target, series):
    closest_index = (series - target).abs().idxmin()
    closest_value = series.loc[closest_index]
    return closest_value
    
if __name__ == "__main__":
    main()