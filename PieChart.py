import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('sleep_data.csv')

# 1. Calculate the total sum for each sleep stage across the entire dataset
total_light_sleep = df['lightsleepduration'].sum()
total_rem_sleep = df['remsleepduration'].sum()
total_deep_sleep = df['deepsleepduration'].sum()
total_waso = df['waso'].sum()

# 2. Create the data for the pie chart
labels = ['Light Sleep', 'REM Sleep', 'Deep Sleep', 'Awake Time\n'
                                                    'after falling asleep']
sizes = [total_light_sleep, total_rem_sleep, total_deep_sleep, total_waso]

colors = ['#87CEEB', '#9370DB', '#4682B4', '#CD5C5C']

# 4. Create the pie chart using Matplotlib
# Create a figure and axis
fig, ax = plt.subplots()

# Draw the pie chart with the new color for 'Awake'
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',  # This adds the percentage labels
    startangle=90,
    colors=colors
)

# Set the title
ax.set_title("Sleep Composition")

# Ensure the pie is drawn as a circle
ax.axis('equal')

# 5. Save the chart as a new PNG file
plt.savefig('sleep_composition_pie_chart.png')