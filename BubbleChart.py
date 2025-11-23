import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Re-loading the data to be safe
df = pd.read_csv('sleep_data.csv')

# Convert waso from seconds to minutes for easier reading
df['waso_minutes'] = df['waso'] / 60

# --- Create Categories (Bins) ---
# 1. Define intervals and labels
bins = [0, 2, 4, 6, 8]
labels = ['< 2 Hours', '2-4 Hours', '4-6 Hours', '> 6 Hours']

# 2. Create the new 'Hour Group' column
# Use right=False to include 0 (e.g., [0-2) )
df['Hour Group'] = pd.cut(df['total_sleep_time_hours'], bins=bins, labels=labels, right=False)

# 3. Define colors for each group
color_map = {
    '< 2 Hours': '#FF5733',  # Red
    '2-4 Hours': '#FFC300',  # Orange
    '4-6 Hours': '#00A8FF',  # Blue
    '> 6 Hours': '#00C853'   # Green
}
# --- End Data Preparation ---


# --- Create Chart (Matplotlib) ---
# Initialize the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Calculate size limits for scaling (similar to Altair)
min_size = 50
max_size = 1000
min_hours = df['total_sleep_time_hours'].min()
max_hours = df['total_sleep_time_hours'].max()

# Plot each group separately to create the color legend
for group, color in color_map.items():
    # Filter data for the current group
    group_data = df[df['Hour Group'] == group]
    if not group_data.empty:
        # Scale bubble sizes (similar to Altair scale(range=[...]))
        scaled_sizes = np.interp(
            group_data['total_sleep_time_hours'],
            [min_hours, max_hours],
            [min_size, max_size]
        )

        ax.scatter(
            group_data['waso_minutes'],
            group_data['sleep_score'],
            s=scaled_sizes,  # Scaled size
            c=color,          # Group color
            label=group,      # Label for the legend
            alpha=0.7,
            edgecolors='w',   # White edge for clarity
            linewidth=0.5
        )

# --- Add Legends and Finalize ---

# 1. Create legend for COLOR (Hour Group)
color_legend = ax.legend(title='Hours Slept Group', loc='upper right')
ax.add_artist(color_legend)  # Add the first legend

# 2. Create legend for SIZE (Hours Slept)
# Create "ghost" points to show the size scale
sizes_for_legend = [2, 4, 6]
legend_handles = []
for size in sizes_for_legend:
    scaled_size = np.interp(size, [min_hours, max_hours], [min_size, max_size])
    legend_handles.append(
        ax.scatter([], [], s=scaled_size, c='gray', label=f'{size} Hours', alpha=0.6)
    )

ax.legend(handles=legend_handles, title='Size (Example)', loc='lower right')

# 3. Set titles and axes
ax.set_title('Sleep Score and Awake Time', fontsize=16)
ax.set_xlabel('Time Spent Awake(Minutes)', fontsize=12)
ax.set_ylabel('Sleep Score', fontsize=12)
ax.set_ylim(0, 100)  # Set Y-axis from 0 to 100
ax.grid(True, linestyle='--', alpha=0.6)  # Add a grid

# Save the chart
plt.savefig('bubble_chart.png')
