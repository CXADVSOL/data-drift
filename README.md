# data-drift
Servers to detect data drift based on KS Test; PSI; Chi-Squared Test

# Analysis of Data Drift Scripts

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



