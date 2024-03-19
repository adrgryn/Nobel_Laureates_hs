Nobel Laureates

This program loads a dataset from a JSON file, performs data exploration, and visualizes the data using various types of charts.

Installation
No installation is required. Simply clone the repository or download the files to your local machine.

Usage
Load the dataset from the JSON file.
Explore the data to get information about its dimensions, data types, and non-null values.
View the percentage participation of countries in the Nobel Prize.
See the total count of male and female Nobel Prize winners by categories.
Analyze the distribution of ages by category using a box plot.
To run the program, execute the main() function in the main.py file.

Dependencies
This program relies on two main modules:
data: Contains functions to load and preprocess the dataset.
charts: Contains functions to create different types of charts for data visualization.

Example Usage
python
Copy code
import data
import charts

# Load the dataset from the JSON file
df = data.create_df()
data.fill_born_in_empty_values(df)

# Explore the DataFrame
display_dataframe_info(df)

# View percentage participation of countries
charts.pie_chart(df)
![image](https://github.com/adrgryn/Nobel_Laureates_hs/assets/87693497/cb3f3b6b-f2d7-47c5-ab19-064e08493d39)

# See total count of male and female Nobel Prize winners by categories
charts.bar_chart(df)
![image](https://github.com/adrgryn/Nobel_Laureates_hs/assets/87693497/48bbdf8e-755b-43f2-bbed-dc60817c718a)

# Analyze distribution of ages by category
charts.boxplot(df)
