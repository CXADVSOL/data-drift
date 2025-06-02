# Prior to using this script, export the following:
# export SPLUNK_ACCESS_TOKEN="<your-token-here>"
# for instance https://api.us1.signalfx.com/GNds_HQA4AE
# Token Otel-Data-Drift-Ingest

# Import the appropriate libraries
import os
import glob
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp

# OpenTelemetry required imports
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# OpenTelemetry Setup
exporter = OTLPMetricExporter(
    endpoint="https://api.us1.signalfx.com/v2/otlp",
    headers={"X-SF-TOKEN": os.getenv("SPLUNK_ACCESS_TOKEN")}
)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=10000)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("forestfires-drift-monitor")

drift_counter = meter.create_counter(
    name="forestfires_drifted_columns",
    description="Number of numeric features with significant drift"
)
p_value_gauge = meter.create_observable_gauge(
    name="forestfires_ks_p_value",
    description="KS test p-value for each numeric feature",
    callbacks=[]
)

# Step 1: Preprocess UCI Forest Fires Dataset
forest_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv"
forest_df = pd.read_csv(forest_url)
print(forest_df.head())

# Find the latest forestfires_*.csv in ./data
csv_files = glob.glob("./data/forestfires_*.csv")
latest_file = max(csv_files, key=os.path.getmtime)
forest_csv_path = latest_file
print(f"Using latest dataset file: {forest_csv_path}")

forest_df1 = pd.read_csv(forest_csv_path)
forest_df1.to_csv(forest_csv_path, index=False)
print(forest_df1.head())

# Encode month/day to numeric
month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
day_map = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}
forest_df['month'] = forest_df['month'].map(month_map)
forest_df['day'] = forest_df['day'].map(day_map)

# Combine datasets
print("Columns in df:", forest_df.columns)
print("Columns in df1:", forest_df1.columns)
print("Shape of df:", forest_df.shape)
print("Shape of df1:", forest_df1.shape)
combined_df = pd.concat([forest_df, forest_df1], ignore_index=True)
print("Combined dataframe head:\n", combined_df.head())
print("Combined dataframe tail:\n", combined_df.tail())
print("Shape of combined_df:", combined_df.shape)

# Plot distributions
numeric_cols = ['X', 'Y', 'month', 'day', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area']
for col in numeric_cols:
    plt.figure(figsize=(10, 5))
    sns.histplot(forest_df[col], kde=True, color='blue', label='forest_df', stat='density', common_norm=False)
    sns.histplot(forest_df1[col], kde=True, color='red', label='forest_df1', stat='density', common_norm=False)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Density')
    plt.legend()
    plt.show()

# Clean numeric columns to ensure no strings are present
for col in numeric_cols:
    forest_df[col] = pd.to_numeric(forest_df[col], errors='coerce')
    forest_df1[col] = pd.to_numeric(forest_df1[col], errors='coerce')

# Optionally drop rows with NaN in numeric columns
forest_df.dropna(subset=numeric_cols, inplace=True)
forest_df1.dropna(subset=numeric_cols, inplace=True)

# KS Test
print("\nKolmogorov-Smirnov Test Results:")
drifted_features = 0
p_values = {}

for col in numeric_cols:
    ks_statistic, p_value = ks_2samp(forest_df[col], forest_df1[col])
    print(f"Column: {col}")
    print(f"  KS Statistic: {ks_statistic:.4f}")
    print(f"  P-value: {p_value:.4f}")
    if p_value < 0.05:
        print(f"  The two distributions for {col} are significantly different.")
        drifted_features += 1
    else:
        print(f"  The two distributions for {col} are not significantly different.")
    p_values[col] = p_value
    print("-" * 20)

# Send metrics to Splunk Observability
drift_counter.add(drifted_features, attributes={"dataset": "forestfires"})

def p_value_callback(options):
    measurements = []
    for feature, p_val in p_values.items():
        measurements.append((p_val, {"feature": feature}))
    return measurements

p_value_gauge = meter.create_observable_gauge(
    name="forestfires_ks_p_value",
    description="KS test p-value for each numeric feature",
    callbacks=[p_value_callback]
)

print(" Drift metrics sent to Splunk Observability.")
