import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch


def plot_sleep_data_with_aggregation_and_ma(file_path):
    """
    Loads sleep data, aggregates multiple sleep episodes per day by summing
    their durations, plots the total daily sleep time, adds a 7-day moving average,
    highlights custom periods, and ensures daily ticks on the x-axis.

    Args:
        file_path (str): The path to the CSV file containing sleep data.
    """
    try:
        # 1. Load the data
        df = pd.read_csv(file_path)

        # 2. Data Preparation: Convert date column to datetime objects
        df['date'] = pd.to_datetime(df['date'])

        # 3. Aggregate data by day
        df_agg = df.groupby('date')['total_sleep_time_hours'].sum().reset_index()

        # --- NEW STEP: Calculate 7-day moving average ---
        # 4. Sort by date first to ensure correct rolling calculation
        df_agg = df_agg.sort_values(by='date')

        # 5. Calculate the 7-day rolling mean.
        # min_periods=1 allows the average to be calculated from the first day.
        df_agg['7_day_moving_avg'] = df_agg['total_sleep_time_hours'].rolling(window=7, min_periods=1).mean()
        # --- END NEW STEP ---

        # 6. Define the user-specified highlight periods
        user_highlight_periods = [
            ('2025-10-18', '2025-10-19'),  # Covers Oct 18, 19
            ('2025-10-25', '2025-10-26'),  # Covers Oct 25, 26
            ('2025-11-01', '2025-11-02'),  # Covers Nov 1, 2
            ('2025-11-08', '2025-11-09')  # Covers Nov 8, 9
        ]
        highlight_periods = [(pd.to_datetime(start), pd.to_datetime(end))
                             for start, end in user_highlight_periods]

        # 7. Prepare the plot
        fig, ax = plt.subplots(figsize=(14, 7))

        # 8. Highlight the user-specified periods
        for start_date, end_date in highlight_periods:
            ax.axvspan(start_date, end_date, color='purple', alpha=0.3, zorder=1)

        # 9. Plot the *aggregated* total sleep time line
        # --- MODIFICATION: Added label ---
        ax.plot(df_agg['date'], df_agg['total_sleep_time_hours'], marker='o', linestyle='-', color='skyblue', zorder=5,
                label='Daily Total Sleep')

        # 10. Plot the 7-day moving average line
        ax.plot(df_agg['date'], df_agg['7_day_moving_avg'], color='orange', linestyle='-', linewidth=2.5,
                label='7-Day Moving Avg', zorder=6)
        # --- END MODIFICATION ---

        # 11. X-Axis Formatting for Every Day
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

        # 12. Add plot elements
        ax.set_title('Daily Total Sleep Time highlighting the weekends', fontsize=16)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Total Sleep Time', fontsize=12)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right')

        # Add a grid
        ax.grid(True, linestyle='--', alpha=0.6, zorder=0)

        # --- MODIFIED STEP: Create combined legend ---
        # 13. Get handles and labels from the plot
        handles, labels = ax.get_legend_handles_labels()

        # 14. Add the custom highlight patch
        custom_highlight_patch = Patch(color='purple', alpha=0.3, label='Weekends days')
        handles.append(custom_highlight_patch)

        # 15. Create the legend
        ax.legend(handles=handles, loc='lower left')
        # --- END MODIFIED STEP ---

        # 16. Set x and y limits based on *aggregated* data
        date_min = df_agg['date'].min() - pd.Timedelta(hours=12)
        date_max = df_agg['date'].max() + pd.Timedelta(hours=12)
        ax.set_xlim(date_min, date_max)
        min_sleep = df_agg['total_sleep_time_hours'].min()
        ax.set_ylim(bottom=max(0, min_sleep - 0.5))

        # 17. Improve layout and save
        plt.tight_layout()
        plt.savefig('time_series.png')

    except FileNotFoundError:
        print(f"Error: File not found at path {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Call the function to run the visualization
plot_sleep_data_with_aggregation_and_ma('sleep_data.csv')