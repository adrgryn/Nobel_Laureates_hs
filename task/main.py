import pandas as pd
import os
import requests
import sys
import data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 1.Load th dataset from the JSON file
df = data.create_df()

# 2. Explore the data
# print(df.axes)
# print(df.shape)
# print(df.info())

# 3. Check for Duplicate Rows
has_duplicates = df.duplicated().any()
data.fill_born_in_empty_values(df)

data.pie_char(df)
data.bar_char(df)
data.boxplot(df)

