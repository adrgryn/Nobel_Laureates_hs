import pandas as pd
import data
import matplotlib.pyplot as plt
import numpy as np

def pie_char(df):
    # set a pie char
    data.unique_country_name(df)
    df['year_born'] = df['date_of_birth'].apply(data.extract_year)
    df['age_of_winning'] = df['year'] - df['year_born']

    # count number of country
    country_counts = df['born_in'].value_counts()

    # country with less than 25 nobel birth
    small_country = country_counts[country_counts < 25].index

    # change to other country
    df['born_in'] = df['born_in'].apply(lambda x: 'Other countries' if x in small_country else x)

    dict_country_values = df['born_in'].value_counts().to_dict()

    labels = []
    sizes = []
    for values, keys in dict_country_values.items():
        labels.append(str(values))
        sizes.append(int(keys))

    explode = [0.0 if label in ['Other countries', 'USA', 'Germany'] else 0.08 for label in labels]

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
    data.unique_country_name(df)

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
