import pandas as pd

df = pd.read_csv("outputs_eval/a2c_netto_eval_conn0_ep0.csv")
# df = pd.read_csv("outputs/metrics.csv")
# df = pd.read_csv("outputs/a2c_ABS_conn0_ep2.csv")
print("Available columns:\n", df.columns.tolist())
print("\nFirst few rows:\n", df.head())

