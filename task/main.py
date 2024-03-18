import data
import charts


# 1.Load th dataset from the JSON file
df = data.create_df()
data.fill_born_in_empty_values(df)
# 2. Explore the data

while True:
    print("""1. Info about DataFrame,
2. Countries percentage participation in nobel prize,
3. The total count of male and female Nobel Prize winners by categories,
4. Distribution of Ages by Category,
0. Exit""")
    user_choice = input()
    if user_choice == "1":
        print(f"Dimensions of the DataFrame:\nrows: {df.shape[0]},\ncolumns: {df.shape[1]}\n\n")
        print("List of axis labels for DataFrame")
        print(df.axes)
        print("\n\nSummary of DataFrame, including info about data types, non-null values and memory usage")
        print(df.info())
    elif user_choice == "2":
        charts.pie_char(df)
    elif user_choice == "3":
        charts.bar_char(df)
    elif user_choice == "4":
        charts.boxplot(df)
    elif user_choice == "0":
        break
    else:
        print("Please enter 1, 2, 3, 4 to display proper chart or 0 to exit")
