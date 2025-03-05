import os
import glob
import matplotlib.pyplot as plt
import pandas as pd

DIRECTORY = "summary\\ingo\\"
INPUT_FILE = os.path.join(DIRECTORY, "all.csv")
INITIAL_DIRECTORY = os.path.join(DIRECTORY, "initial.csv")
OPTIMUM_DIRECTORY = os.path.join(DIRECTORY, "optimum.csv")
RECOVERY_DIRECTORY = os.path.join(DIRECTORY, "recovery.csv")
DROP_DIRECTORY = os.path.join(DIRECTORY, "drop.csv")

non_rl_model_names = ["maxpressure", "fixedtime"]

case_mapping = {
    "ingo_morning": 1,
    "ingo_noon": 2,
    "ingo_evening": 3,
    "ingo_sensor": 4,
}

# open the file and load into a pandas dataframe
df = pd.read_csv(INPUT_FILE, index_col=False)

df["case"] = df["case"].map(case_mapping)


pivot_df = df.pivot(index="case", columns="model_name")

model_names = ["dqn", "colight"]


initial_travel_time = pivot_df['initial_travel_time'].reindex(columns=model_names)
min_travel_time = pivot_df['optimum_travel_time'].reindex(columns=model_names)
recovery_time = pivot_df['recovery_time'].reindex(columns=model_names)
initial_drop = pivot_df['initial_drop'].reindex(columns=model_names)

initial_travel_time.to_csv(INITIAL_DIRECTORY)
min_travel_time.to_csv(OPTIMUM_DIRECTORY)
recovery_time.to_csv(RECOVERY_DIRECTORY)
initial_drop.to_csv(DROP_DIRECTORY)

print("done")
