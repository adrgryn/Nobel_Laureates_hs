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

def pie_char(df):
    # set a pie char
    unique_country_name(df)
    # print(df.columns.values.tolist())
    # print(df['date_of_birth'])
    df['year_born'] = df['date_of_birth'].apply(extract_year)
    # print(df['year_born'].tolist())

    df['age_of_winning'] = df['year'] - df['year_born']
    # print(df['age_of_winning'].tolist())

    # count number of country
    country_counts = df['born_in'].value_counts()

    # country with less than 25 nobel birth
    small_country = country_counts[country_counts < 25].index

    # change to other country
    df['born_in'] = df['born_in'].apply(lambda x: 'Other countries' if x in small_country else x)

    dict_country_values = df['born_in'].value_counts().to_dict()
    # labels = [lambda x: x for keys in dict_country_values.keys()]
    # sizes = [lambda x: x for values in dict_country_values.values()]
    labels = []
    sizes = []
    for values, keys in dict_country_values.items():
        labels.append(str(values))
        sizes.append(int(keys))
    # print(labels)
    explode = [0.0 if label in ['Other countries', 'USA', 'Germany'] else 0.08 for label in labels]
    # print(sizes)
    # print(dict_country_values)
    colors = ['blue', 'orange', 'red', 'yellow', 'green', 'pink', 'brown', 'cyan', 'purple']
    total_laureates = sum(sizes)
    plt.figure(figsize=(12, 12))
    plt.pie(sizes, labels=labels, explode=explode, colors=colors, autopct=lambda pct:
    '{:.2f}%\n({:.0f})'.format(pct, pct * total_laureates / 100))

    plt.show()


def bar_char(df):

    def lst_of_columns_values(lst_name: str) -> list:
        columns_values_lst = []
        values = df[lst_name].to_list()
        for value in values:
            if value not in columns_values_lst :
                columns_values_lst.append(value)

        return sorted(columns_values_lst)

    unique_country_name(df)

    # drop all rows without values for category columns
    df = df[df['category'].str.strip() != '']

    # count all men for each category
    male_df = df[df['gender'] == 'male']
    male_category_counts = male_df.groupby('category')['gender'].count()

    # count all women for each category
    female_df = df[df['gender'] == 'female']
    female_category_counts = female_df.groupby('category')['gender'].count().tolist()

    # set  bar chart

    categories = lst_of_columns_values('category')
    male = male_category_counts
    female = female_category_counts

    # colors = ['blue', 'crimson']

    x_axis = np.arange(len(categories))

    plt.figure(figsize=(10, 10))

    plt.bar(x_axis-0.2, male, color='blue', width=0.4, label='Males')
    plt.bar(x_axis+0.2, female, color='crimson', width=0.4, label='Females')

    plt.xticks(x_axis, categories)
    plt.xlabel("Category", fontsize=14)
    plt.ylabel("Nobel Laureates Count", fontsize=14)
    plt.title("The total count of male and female Nobel Prize winners by categories", fontsize=20)
    plt.legend()
    plt.yticks(range(0, 225, 25))

    plt.show()

def boxplot(df):
    # age = df['age_of_winning'].groupby('category')['age_of_wining'].count()
    df = df.assign(age_of_winning=df['age_of_winning'])
    # Calculate mean age for each category
    mean_age_by_category = df.groupby('category')['age_of_winning'].mean()

    df_all = pd.concat([df, df.assign(category='All categories')])
    sorted_categories = sorted(df_all['category'].unique().tolist())
    sorted_categories.remove('All categories')
    sorted_categories.append('All categories')

    plt.figure(figsize=(10, 10))
    labels = sorted_categories

    # Create a list of arrays for boxplot
    boxplot_data = []
    for category in sorted_categories:
        boxplot_data.append(df_all[df_all['category'] == category]['age_of_winning'])

    plt.boxplot(boxplot_data, labels=labels,
                medianprops=dict(color='orange'),
                showmeans=True)

    plt.xlabel('Category', fontsize=14)
    plt.ylabel('Age of obtaining the Nobel Prize', fontsize=14)
    plt.title("Distribution of Ages by Category", fontsize=20)

    plt.xticks(range(1, len(sorted_categories) + 1), sorted_categories, fontsize=14)

    plt.show()
