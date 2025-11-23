import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator # Import the locator

# Load the data
df = pd.read_csv('sleep_data.csv')

# Convert waso from seconds to minutes
df['waso_minutes'] = df['waso'] / 60

# --- Filter the data ---
# Keep only the rows where 'waso_minutes' is greater than 0
df_filtered = df[df['waso_minutes'] > 0].copy()

# --- Create the plot ---
fig, ax = plt.subplots()

# 1. Create the scatter plot using the filtered data
ax.scatter(df_filtered['waso_minutes'], df_filtered['sleep_score'], alpha=0.7)

# 2. Calculate and create the trend line
df_clean = df_filtered.dropna(subset=['waso_minutes', 'sleep_score'])
if not df_clean.empty and len(df_clean) > 1:
    m, b = np.polyfit(df_clean['waso_minutes'], df_clean['sleep_score'], 1)
    x_line = np.array([df_clean['waso_minutes'].min(), df_clean['waso_minutes'].max()])
    y_line = m * x_line + b
    ax.plot(x_line, y_line, color='red', linestyle='--')

# 3. Set the titles and labels
ax.set_title('Sleep Score and Awake Time')
ax.set_xlabel('Minutes spent awake after falling asleep')
ax.set_ylabel('Sleep Score')

# 4. Set the Y-axis (Sleep Score) from 0 to 100
ax.set_ylim(0, 100)

# 5. Set the X-axis (Minute) intervals every 10 minutes
ax.xaxis.set_major_locator(MultipleLocator(10))

# 6. Save the chart as a PNG file
plt.savefig('scatterplot.png')
