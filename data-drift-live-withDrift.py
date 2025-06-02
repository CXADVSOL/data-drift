# Import necessary packages after kernel reset
import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

# Splunk Observability Cloud Otel tracing
from splunk_otel.tracing import start_tracing

start_tracing()

# Also accepts optional settings. For example:
#
# start_tracing(
#   service_name='<my-python-service>',
#   span_exporter_factories=[OTLPSpanExporter]
#   access_token='<access_token>',
#   max_attr_length=12000,
#   trace_response_header_enabled=True,
#   resource_attributes={
#    'service.version': '<your_version>',
#    'deployment.environment': '<your_environment>',
#  })

# Step 1: Preprocess UCI Forest Fires Live Dataset
forest_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv"
forest_df = pd.read_csv(forest_url)
print(forest_df.head())

# Find the most recent forestfires_*.csv file in ./data
csv_files = glob.glob("./data/forestfires_*.csv")
latest_file = max(csv_files, key=os.path.getmtime)  # find latest by modification time
forest_csv_path = latest_file
print(f"✅ Using latest dataset file: {forest_csv_path}")

forest_df1 = pd.read_csv(forest_csv_path)
forest_df1.to_csv(forest_csv_path, index=False)
print(forest_df1.head())


# Encode month and day to numerical values for modeling
month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5,
             'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10,
             'nov': 11, 'dec': 12}
day_map = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}

forest_df['month'] = forest_df['month'].map(month_map)
forest_df['day'] = forest_df['day'].map(day_map)

# Combine df and df1 data frames

# Check the column names of both dataframes
print("Columns in df:", forest_df.columns)
print("Columns in df1:", forest_df1.columns)

# Check the shapes of the dataframes
print("Shape of df:", forest_df.shape)
print("Shape of df1:", forest_df1.shape)

# Combine dataframes using concat.
# We'll concatenate them row-wise.
# Use axis=0 for concatenation along rows.
combined_df = pd.concat([forest_df, forest_df1], ignore_index=True)

# Display the head of the combined dataframe to see the result
print("Combined dataframe head:")
print(combined_df.head())

# Display the tail of the combined dataframe to see the result
print("Combined dataframe tail:")
print(combined_df.tail())

# Display the shape of the combined dataframe
print("Shape of combined_df:", combined_df.shape)

# Plot the distributions of df and df1

# Select a few numeric columns for plotting
numeric_cols = ['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area']

# Plot distributions for selected numeric columns
for col in numeric_cols:
    plt.figure(figsize=(10, 5))
    sns.histplot(forest_df[col], kde=True, color='blue', label='forest_df', stat='density', common_norm=False)
    sns.histplot(forest_df1[col], kde=True, color='red', label='forest_df1', stat='density', common_norm=False)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Density')
    plt.legend()
    plt.show()

# For categorical columns, we can plot counts
categorical_cols = ['month', 'day'] # Assuming month and day are treated as categorical in original df1 but numeric in df

# Perform the KS Test for df and df1

# Select a few numeric columns for KS test
numeric_cols = ['X', 'Y', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area']

# Perform KS test for selected numeric columns
print("\nKolmogorov-Smirnov Test Results:")
for col in numeric_cols:
    ks_statistic, p_value = ks_2samp(forest_df[col], forest_df1[col])
    print(f"Column: {col}")
    print(f"  KS Statistic: {ks_statistic:.4f}")
    print(f"  P-value: {p_value:.4f}")
    # Interpret the result (common alpha is 0.05)
    alpha = 0.05
    if p_value < alpha:
        print(f"  The two distributions for {col} are significantly different.")
    else:
        print(f"  The two distributions for {col} are not significantly different.")
    print("-" * 20)
