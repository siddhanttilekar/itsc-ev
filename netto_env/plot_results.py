import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths
rl_eval_file = "outputs/a2c_netto_conn0_ep1000.csv"  # After training
baseline_file = "outputs/a2c_netto_conn0_ep1.csv"            # Before training (Round Robin or default)

# Load RL evaluation results
df_rl = pd.read_csv(rl_eval_file)

# Load baseline (before training) results
if os.path.exists(baseline_file):
    df_base = pd.read_csv(baseline_file)
else:
    raise FileNotFoundError(f"Baseline file not found: {baseline_file}")

# Plot: Mean Waiting Time and Stopped Vehicles
plt.figure(figsize=(12, 6))

# Plot 1: Mean Waiting Time
plt.subplot(1, 2, 1)
plt.plot(df_base["step"], df_base["system_mean_waiting_time"], color="gray", linestyle='--', label="Before Training")
plt.plot(df_rl["step"], df_rl["system_mean_waiting_time"], color="blue", label="After Training (A2C)")
plt.xlabel("Simulation Step")
plt.ylabel("Mean Waiting Time (s)")
plt.title("System Mean Waiting Time per Step")
plt.legend()

# Plot 2: Stopped Vehicles
plt.subplot(1, 2, 2)
plt.plot(df_base["step"], df_base["system_total_stopped"], color="gray", linestyle='--', label="Before Training")
plt.plot(df_rl["step"], df_rl["system_total_stopped"], color="red", label="After Training (A2C)")
plt.xlabel("Simulation Step")
plt.ylabel("Number of Stopped Vehicles")
plt.title("System Total Stopped Vehicles per Step")
plt.legend()

plt.tight_layout()
plt.show()
