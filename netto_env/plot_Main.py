
# Divided 3 KPI
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('outputs_eval/a2c_netto_eval_conn0_ep0.csv')
# data = pd.read_csv('outputs/a2c_ABS_conn0_ep2.csv')
# data = pd.read_csv('output_simulation.csv')

# Extract relevant columns
steps = data['step']
avg_speed = data['system_mean_speed']
queue_length = data['system_total_stopped']
avg_waiting_time = data['system_mean_waiting_time']  # Avg Waiting Time column

# Assuming 'agents_total_stopped' can be used as a proxy for collisions or 'collisions' column is available elsewhere
# If there is no separate 'collisions' column, you can use 'agents_total_stopped' for illustration
collisions = data['agents_total_stopped']  # Update this to actual collisions column if present

# Create subplots (1 row, 3 columns)
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot Avg Queue Length
axs[0].plot(steps, queue_length, label="Avg Queue Length", color='blue')
axs[0].set_title('Avg Queue Length')
axs[0].set_xlabel('Step')
axs[0].set_ylabel('Vehicle Count')
axs[0].grid(True)

# Plot Collisions
axs[1].plot(steps, collisions, label="Collisions", color='red')
axs[1].set_title('Collisions')
axs[1].set_xlabel('Step')
axs[1].set_ylabel('Collisions Count')
axs[1].grid(True)

# Plot Avg Waiting Time
axs[2].plot(steps, avg_waiting_time, label="Avg Waiting Time", color='green')
axs[2].set_title('Avg Waiting Time')
axs[2].set_xlabel('Step')
axs[2].set_ylabel('Seconds')
axs[2].grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()


