import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = 'sleep_data.csv'
try:
    df = pd.read_csv(file_path)

    potential_cols = [
        'sleep_score',
        'total_timeinbed',
        'total_sleep_time',
        'lightsleepduration',
        'remsleepduration',
        'deepsleepduration',
        'sleep_efficiency',
        'wakeupcount',
        'waso',
        'nb_rem_episodes',
        'hr_average',
        'rr_average',
        'snoring'
    ]

    # Find which of these potential columns are actually in the DataFrame
    cols_to_use = [col for col in potential_cols if col in df.columns]

    col_to_remove = 'total_sleep_time_hours'
    if col_to_remove in cols_to_use:
        cols_to_use.remove(col_to_remove)
    else:
        print(f"Note: '{col_to_remove}' was not in the list of columns to plot anyway.")

    if not cols_to_use:
        print("Error: No relevant columns left to create a heatmap.")
    else:
        for col in cols_to_use:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Drop rows where *any* of our selected columns have a NaN value
        df_cleaned = df[cols_to_use].dropna()

        print(f"Original row count: {len(df)}, Cleaned row count: {len(df_cleaned)}")

        if len(df_cleaned) < 2:
            print("Error: Not enough valid data to create a heatmap after cleaning.")
        else:
            # --- Calculate Correlation Matrix ---
            corr_matrix = df_cleaned.corr()

            # --- Create the Heatmap ---
            plt.figure(figsize=(14, 10))  # Make the figure larger

            sns.heatmap(
                corr_matrix,
                annot=True,
                fmt='.2f',
                cmap='vlag',
                center=0,
                linewidths=.5,
                cbar_kws={"shrink": .8}
            )

            # Adjust title and layout
            plt.title('Correlation Heatmap of Sleep Metrics', fontsize=16)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout()

            # Save the plot to a file
            heatmap_filename = 'sleep_metrics_heatmap.png'
            plt.savefig(heatmap_filename)

            print(f"Modified heatmap saved as '{heatmap_filename}'")
            print(corr_matrix)

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")