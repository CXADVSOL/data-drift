import os
import requests
from datetime import datetime

# URL of the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv"

# Create the data directory if it doesn't exist
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# Generate the timestamp string
timestamp = datetime.utcnow().strftime("%d%B%Y%H%MUTC")  # e.g., 1June20251551UTC

# Create the filename
filename = f"forestfires_{timestamp}.csv"
file_path = os.path.join(data_dir, filename)

# Download the dataset
response = requests.get(url)
if response.status_code == 200:
    with open(file_path, "wb") as f:
        f.write(response.content)
    print(f"Dataset saved as {file_path}")
else:
    print(f"Failed to download the dataset. Status code: {response.status_code}")
