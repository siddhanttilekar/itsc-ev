
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from sumo_env_wrapper import SumoRLWrapper
import os
import sys

# SUMO tools path
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

def make_env():
    return SumoRLWrapper(
        net_file="Network files/expjac.net.xml",
        route_file="Network files/ABS_intersection.rou.xml",
        out_csv_name="outputs/a2c_ABS",
        single_agent=True,
        use_gui=False,
        num_seconds=1900,
    )

env = DummyVecEnv([make_env])
model = A2C("MlpPolicy", env, verbose=1)

EPISODES = 10
TIMESTEPS_PER_EPISODE = 2000

for ep in range(1, EPISODES + 1):
    print(f"▶ Training Episode {ep}")
    model.learn(total_timesteps=TIMESTEPS_PER_EPISODE, reset_num_timesteps=False)
    env.envs[0].write_episode_metrics(ep)

model.save("models/a2c_ABS_model")
env.envs[0].close()
