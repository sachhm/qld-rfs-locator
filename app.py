import pandas as pd
import requests

# read data as dataframe
qld_rfs = pd.read_csv("data/qld-rfs.csv")

street_no = float(input("Enter your street number "))
street = input("Enter your street ")
locality = input("Enter your locality ")  

street = street.replace(" ", "+")
locality = locality.replace(" ", "+")


geocoding_request_url = f'https://photon.komoot.io/api/?q={street_no}+{street}+{locality}'

geocoding_request = requests.get(geocoding_request_url)
print(geocoding_request_url)
