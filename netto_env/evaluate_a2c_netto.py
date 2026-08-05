from stable_baselines3 import A2C
from sumo_rl import SumoEnvironment
import os

# Create the output folder if it doesn't exist
os.makedirs("outputs_eval", exist_ok=True)

# Create the SUMO evaluation environment
env = SumoEnvironment(
    net_file="Network files/expjac.net.xml",
    route_file="Network files/ABS_intersection.rou.xml",
    out_csv_name="outputs_eval/a2c_ABS_eval",  # Output will be a2c_netto_eval.csv
    use_gui=True,
    num_seconds=1900,
    single_agent=True,
    yellow_time=3,
    min_green=5,
)

# Load the best trained model
model = A2C.load("models/a2c_ABS_model", device="cpu")

# Evaluate the model
try:
    obs, info = env.reset()
    done = False
    total_reward = 0
    step = 0

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward
        step += 1
        print(f"Step: {step}, Reward: {reward}, Done: {done}")

    print(f"Evaluation completed. Total reward: {total_reward}")

finally:
    # Save the results and metrics
    env.save_csv(out_csv_name="outputs_eval/a2c_netto_eval", episode=0)
    env.close()
