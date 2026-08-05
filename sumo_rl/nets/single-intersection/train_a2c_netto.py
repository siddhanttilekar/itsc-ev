import os
import numpy as np
from stable_baselines3 import A2C
from sumo_rl import SumoEnvironment
import traci

# Initialize the SUMO RL environment
env = SumoEnvironment(
    net_file="single-intersection.net.xml",
    route_file="single-intersection.rou.xml",
    out_csv_name="outputs/a2c_netto",
    use_gui=False,
    num_seconds=1000,
    single_agent=True,
    yellow_time=3,
    min_green=5,
    reward_fn="pressure"
)

# Print traffic signal info
print("✅ Traffic Signal IDs:", env.ts_ids)
ts_id = env.ts_ids[0]

# Start SUMO simulation to inspect signal phases
env.reset()
phases = traci.trafficlight.getAllProgramLogics(ts_id)[0].phases
print(f"✅ Number of parsed phases: {len(phases)}")
print("✅ Parsed Phases:")
for i, p in enumerate(phases):
    print(f"  Phase {i}: {p.state} | Duration: {p.duration}")

# (Optional) Step through a few seconds to inspect initial behavior
for _ in range(20):  # Do NOT run for 1000 steps, or SUMO will end before training
    print("Current phase index:", traci.trafficlight.getPhase(ts_id))
    traci.simulationStep()

# Reset the environment before training
env.reset()

# Train the model
model = A2C("MlpPolicy", env, verbose=1)
try:
    model.learn(total_timesteps=10000, reset_num_timesteps=False)
finally:
    env.close()

# Save the trained model
model.save("a2c_netto_model")




# Waiting time 


# # Set up SUMO-RL environment with waiting time KPI
# env = SumoEnvironment(
#     net_file="netto.net.xml",
#     route_file="netto.rou.xml",
#     out_csv_name="outputs/a2c_netto_waiting_time",
#     use_gui=False,  # set to False if running headless
#     num_seconds=1000,
#     single_agent=True,
#     yellow_time=3,
#     min_green=5,
#     reward_fn="waiting_time"  # Use waiting time as reward KPI
# )

# # Train A2C model
# model = A2C("MlpPolicy", env, verbose=1)

# try:
#     model.learn(total_timesteps=20000, reset_num_timesteps=False)
# finally:
#     env.close()

# # Save trained model
# model.save("a2c_netto_model_waiting_time")



# New Code 


# # Optional: Disable SUMO's internal randomness
# os.environ["SUMO_RANDOM"] = "0"

# # Run training over multiple seeds
# for seed in [0, 42, 123]:
#     print(f"\n🚦 Training with seed {seed}...\n")

#     # Set Python and NumPy random seeds (optional for full reproducibility)
#     random.seed(seed)
#     np.random.seed(seed)

#     env = SumoEnvironment(
#         net_file="netto.net.xml",
#         route_file="netto.rou.xml",
#         out_csv_name=f"outputs/a2c_netto_seed{seed}",
#         use_gui=False,
#         num_seconds=1000,
#         single_agent=True,
#         yellow_time=3,
#         min_green=5,
#         reward_fn="pressure"
#     )

#     model = A2C(
#         "MlpPolicy",
#         env,
#         verbose=1,
#         seed=seed,
#         learning_rate=0.0003,  # Fine-tuned learning rate
#         n_steps=5              # Batch size per update
#     )

#     try:
#         model.learn(total_timesteps=200000, reset_num_timesteps=False)
#     finally:
#         env.close()

#     model.save(f"a2c_netto_model_seed{seed}")
#     print(f"Saved model for seed {seed}")




# import gymnasium as gym
# import sumo_rl
# env = gym.make('sumo-rl-v0',
#                 net_file="single-intersection.net.xml",
#                 route_file="single-intersection.rou.xml",
#                 out_csv_name='outputs/a2c_netto',
#                 use_gui=True,
#                 num_seconds=1900)
# obs, info = env.reset()
# done = False
# while not done:
#     next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
#     done = terminated or truncated