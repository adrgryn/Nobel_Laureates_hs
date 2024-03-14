import os
import sys
import requests
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the Data directory
data_dir = os.path.join(script_dir, 'Data')

# Create the Data directory if it does not exist
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# Download data if it is unavailable.
data_path = os.path.join(data_dir, 'Nobel_laureates.json')
if not os.path.isfile(data_path):  # Corrected this line
    sys.stderr.write("[INFO] Dataset is loading.\n")
    url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
    r = requests.get(url, allow_redirects=True)
    with open(data_path, 'wb') as f:
        f.write(r.content)
    sys.stderr.write("[INFO] Loaded.\n")


def create_df():
    df = pd.read_json(data_path)
    return df


def extract_birth_country(df) -> list:
    list_of_places = []
    birth_place = df[['place_of_birth']].to_numpy()
    for place in birth_place:
        if len(place) >= 1:
            list_of_places.append(place[-1])
        else:
            list_of_places.append(None)
    return list_of_places


def fill_empty_values(df, list_of_places):
    born_in = df[['born_in']].to_numpy()
