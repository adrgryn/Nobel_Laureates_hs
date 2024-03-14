import pandas as pd
import os
import requests
import sys
import data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

# write your code here

# 1.Load th dataset from the JSON file
df = data.create_df()

# 2. Explore the data

# print(df.axes)
# print(df.shape)
# print(df.info())

# 3. Check for Duplicate Rows
has_duplicates = df.duplicated().any()

# 4. Drop Rows Where the Gender Column Has Missing Values
df = df.dropna(subset=['gender'])

# 5. Re-index the DataFrame
df.reset_index(drop=True, inplace=True)


# Output the result according to task requirements
# print(has_duplicates)
# print(df[['country', 'name']].head(20).to_dict())

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


def lst_of_columns_values(lst_name: str) -> list:
    columns_values_lst = []
    values = df[lst_name].to_list()
    for value in values:
        if value not in columns_values_lst:
            columns_values_lst.append(value)

    return sorted(columns_values_lst)


df['place_of_birth'] = df['place_of_birth'].apply(extract_country)
df['born_in'] = df['born_in'].where(df['born_in'] != '', df['place_of_birth'])
df.dropna(subset=['born_in'], inplace=True)
df.loc[df['born_in'] == 'U.S.', 'born_in'] = 'USA'
df.loc[df['born_in'] == 'US', 'born_in'] = 'USA'
df.loc[df['born_in'] == 'United States', 'born_in'] = 'USA'
df.loc[df['born_in'] == 'United Kingdom', 'born_in'] = 'UK'
born_in_values = df['born_in'].tolist()
# print(df.columns.values.tolist())
# print(df['date_of_birth'])
df['year_born'] = df['date_of_birth'].apply(extract_year)
# print(df['year_born'].tolist())
df['age_of_winning'] = df['year'] - df['year_born']
# print(df['age_of_winning'].tolist())

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

# plt.figure(figsize=(10, 10))
#
# plt.bar(x_axis-0.2, male, color='blue', width=0.4, label='Males')
# plt.bar(x_axis+0.2, female, color='crimson', width=0.4, label='Females')
#
# plt.xticks(x_axis, categories)
# plt.xlabel("Category", fontsize=14)
# plt.ylabel("Nobel Laureates Count", fontsize=14)
# plt.title("The total count of male and female Nobel Prize winners by categories", fontsize=20)
# plt.legend()
# plt.yticks(range(0, 225, 25))

# plt.show()

# age = df['age_of_winning'].groupby('category')['age_of_wining'].count()
df = df.assign(age_of_winning=df['age_of_winning'])

# Calculate mean age for each category
mean_age_by_category = df.groupby('category')['age_of_winning'].mean()

df_all = pd.concat([df, df.assign(category='All categories')])
age_by_category = df_all.groupby('category')['age_of_winning']

sorted_categories = sorted(df_all['category'].unique().tolist())
sorted_categories.remove('All categories')
sorted_categories.append('All categories')
# print(df_all)
# print(sorted_categories)
plt.figure(figsize=(10, 10))
# ax = sns.boxplot(x='category', y='age_of_winning', data=df_all,
#                  order=sorted_categories,
#                  boxprops=dict(facecolor='none'),
#                  medianprops=dict(color='orange'),
#                  showmeans=True,
#                  )
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
