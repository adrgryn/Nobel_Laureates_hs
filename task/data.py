import os
import sys
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    df = df.dropna(subset=['gender'])
    df.reset_index(drop=True, inplace=True)
    return df


def extract_birth_country(df) -> list:
    """Extract country from column 'birth_of_birth'. If no country, place None """
    list_of_places = []
    birth_place = df[['place_of_birth']].to_numpy()
    for place in birth_place:
        if len(place) >= 1:
            list_of_places.append(place[-1])
        else:
            list_of_places.append(None)
    return list_of_places


def fill_born_in_empty_values(df):
    """Fill missing values in 'born_in' column"""
    df['place_of_birth'] = df['place_of_birth'].apply(extract_country)
    df['born_in'] = df['born_in'].where(df['born_in'] != '', df['place_of_birth'])
    # modify df by dropping rows where 'born_in' column contains NaN value
    df.dropna(subset=['born_in'], inplace=True)


def unique_country_name(df):
    """Unifies the country names for the USA and UK"""
    df.loc[df['born_in'] == 'U.S.', 'born_in'] = 'USA'
    df.loc[df['born_in'] == 'US', 'born_in'] = 'USA'
    df.loc[df['born_in'] == 'United States', 'born_in'] = 'USA'
    df.loc[df['born_in'] == 'United Kingdom', 'born_in'] = 'UK'
    born_in_values = df['born_in'].tolist()
    return born_in_values


def fill_empty_values(df, list_of_places):
    born_in = df[['born_in']].to_numpy()


def extract_country(place):
    try:
        parts = place.split(',')
        if len(parts) > 1:
            return parts[-1].strip()
        else:
            return None
    except AttributeError:
        return None


def extract_year(date):
    try:
        year = date.split()
        if len(year) > 1:
            return int(year[-1])
        else:
            return int(date[0:4])
    except AttributeError:
        pass


def operation_on_data_frame(df):
    # specifies new column 'year_born'
    df['year_born'] = df['date_of_birth'].apply(extract_year)
    # specifies new column 'age_of_winning
    df['age_of_winning'] = df['year'] - df['year_born']
    # drop all rows without values for category columns
    df = df[df['category'].str.strip() != '']
    return df


def lst_of_columns_values(lst_name: str) -> list:
    df = create_df()
    columns_values_lst = []
    values = df[lst_name].to_list()
    for value in values:
        if value not in columns_values_lst:
            columns_values_lst.append(value)

    return sorted(columns_values_lst)

