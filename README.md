# data-drift
Servers to detect data drift based on KS Test; PSI; Chi-Squared Test

# Analysis of Data Drift Analysis Servers

### `data-drift-sim.py`
- Uses **Kolmogorov–Smirnov test** to detect drift between datasets.
- Generates **visualizations** (likely KDE plots or histograms).
- Uses **Seaborn KDE plots** to compare distributions visually.
- Outputs statistical test results like **p-values** to indicate drift.

### `data-drift-live-dataset.py`
- Uses **Kolmogorov–Smirnov test** to detect drift between datasets.
- Generates **visualizations** (likely KDE plots or histograms).
- Loads data from CSV files, indicating **dataset-based drift comparison**.
- Outputs statistical test results like **p-values** to indicate drift.
- Applies drift detection to the **forest fires dataset**.
- This script probably applies drift detection to **live or updated data without drift**.

### `data-drift-live-withDrift.py`
- Uses **Kolmogorov–Smirnov test** to detect drift between datasets.
- Generates **visualizations** (likely KDE plots or histograms).
- Loads data from CSV files, indicating **dataset-based drift comparison**.
- Outputs statistical test results like **p-values** to indicate drift.
- Applies drift detection to the **forest fires dataset**.
- This script likely runs drift detection on **live-simulated drifted data**.

# 📓 Analysis of Data Drift Notebooks

### `data-drift-live-dataset.ipynb`
- Applies the **Kolmogorov–Smirnov (KS) test** to detect data drift.
- Loads data from CSV files, suggesting use of pre-recorded or simulated datasets.
- Prints the **p-value** from the KS test to indicate statistical significance of drift.
- Uses the **Forest Fires dataset** as the subject of analysis.
- Purpose: Drift analysis between **realistic but stable live dataset** vs. training baseline.

### `data-drift-sim.ipynb`
- Applies the **Kolmogorov–Smirnov (KS) test** to detect data drift.
- Visualizes feature distributions using **Seaborn KDE plots**.
- Prints the **p-value** from the KS test to indicate statistical significance of drift.
- Purpose: Simulates **intentional drift** in data for demonstration of detection techniques.



```Shell
python3 -m venv DataDrift
source DataDrioft/bin/activate
pip install -r requirements.txt
```

```Python
python3 ./data-drift-live-dataset.py
```
The ouptut of the above dataset analysis will show no drift.

```Python
python3 ./data-drift-live-withDrift.py
```

The output of the above will significant data drift in several of the columns associated with the pre-processed data
