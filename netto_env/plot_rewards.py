
# metrics

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv("outputs/metrics.csv")

# Create the plot
plt.figure(figsize=(10, 5))

# Plot the metrics
plt.plot(df['episode'], df['avg_speed'], label='Average Speed')
plt.plot(df['episode'], df['avg_queue_length'], label='Average Queue Length')
plt.plot(df['episode'], df['total_collisions'], label='Total Collisions')  # Added total collisions and removed teleport

# Set plot title and labels
plt.title("Training Metrics")
plt.xlabel("Episode")
plt.ylabel("Metric Value")

# Customize the grid and legend
plt.grid(True)
plt.legend()

# Adjust the layout for a cleaner look
plt.tight_layout()

# Save the plot as a PNG file
plt.savefig("outputs/training_metrics_plot.png")

# Show the plot
plt.show()





