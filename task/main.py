import data
import charts


# 1.Load th dataset from the JSON file
df = data.create_df()
data.fill_born_in_empty_values(df)
# 2. Explore the data


# Define your DataFrame (df) and any necessary data processing functions here
def display_dataframe_info(df):
    print(f"Dimensions of the DataFrame:\nRows: {df.shape[0]},\nColumns: {df.shape[1]}\n")
    print("List of axis labels for DataFrame:")
    print(df.axes)
    print("\nSummary of DataFrame, including info about data types, non-null values, and memory usage:")
    print(df.info())


def main():
    while True:
        print("""
        Menu:
        1. Info about DataFrame
        2. Countries percentage participation in Nobel Prize
        3. Total count of male and female Nobel Prize winners by categories
        4. Distribution of Ages by Category
        0. Exit
        """)
        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            display_dataframe_info(df)
        elif user_choice == "2":
            charts.pie_char(df)
        elif user_choice == "3":
            charts.bar_char(df)
        elif user_choice == "4":
            charts.boxplot(df)
        elif user_choice == "0":
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    # Initialize your DataFrame (df) here
    main()
