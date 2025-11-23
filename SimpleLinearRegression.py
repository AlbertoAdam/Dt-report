import pandas as pd
from scipy.stats import pearsonr
import numpy as np

# Load the dataset
file_path = 'sleep_data.csv'
try:
    df = pd.read_csv(file_path)

    # Specify the columns of interest
    col1 = 'sleep_score'
    col2 = 'total_sleep_time_hours'

    # Check if columns exist
    if col1 not in df.columns or col2 not in df.columns:
        print(f"Error: One or both columns '{col1}' or '{col2}' not found in the CSV.")
        print(f"Available columns are: {df.columns.tolist()}")
    else:
        # Ensure data is numeric, coercing any errors to NaN
        df[col1] = pd.to_numeric(df[col1], errors='coerce')
        df[col2] = pd.to_numeric(df[col2], errors='coerce')

        # Check for missing values (NaNs) which now include original NaNs and coerced errors
        initial_nans_col1 = df[col1].isnull().sum()
        initial_nans_col2 = df[col2].isnull().sum()

        if initial_nans_col1 > 0 or initial_nans_col2 > 0:
            print(f"Note: Missing or non-numeric values found and removed in '{col1}': {initial_nans_col1}")
            print(f"Note: Missing or non-numeric values found and removed in '{col2}': {initial_nans_col2}")

        # Drop rows where either column has a NaN value
        df_cleaned = df.dropna(subset=[col1, col2])

        # Check if we have enough data to calculate correlation (need at least 2 points)
        if len(df_cleaned) < 2:
            print("Error: Not enough valid data points (less than 2) to calculate correlation.")
        else:
            # Calculate the Pearson correlation coefficient and the p-value
            correlation_coefficient, p_value = pearsonr(df_cleaned[col1], df_cleaned[col2])

            print(f"--- Correlation Analysis Results ---")
            print(f"Variable 1: {col1}")
            print(f"Variable 2: {col2}")
            print(f"Correlation Coefficient (r): {correlation_coefficient}")
            # Format the p-value to display as a fixed-point number (float)
            # Using .30f to show 30 decimal places, which is enough to show its small value
            print(f"P-value: {p_value:.30f}")
            print(f"Number of data points used: {len(df_cleaned)}")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")