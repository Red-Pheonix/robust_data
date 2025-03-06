import os
import glob
import matplotlib.pyplot as plt
import pandas as pd

DIRECTORY = "ingo"
OUTPUT_DIRECTORY = "summary/ingo/"

all_files = glob.glob(os.path.join(DIRECTORY, "**", "*.csv"), recursive=True)
csv_files = [f for f in all_files if "queue" not in os.path.basename(f)]
csv_files.sort()


experiments = {}
experiments["colight"] = {}
experiments["dqn"] = {}
# experiments["mplight"] = {}
experiments["fixedtime"] = {}
experiments["maxpressure"] = {}

for filename in csv_files:
    model_name = filename.split("\\")[1]
    experiment_name = filename.split("\\")[-1].rstrip(".csv")
    dqn_df = pd.read_csv(filename)
    experiments[model_name][experiment_name] = dqn_df


case_names = [
    "ingo_morning",
    "ingo_noon",
    "ingo_evening",
    "ingo_sensor",
]

rl_model_names = [
    "dqn",
    "colight",
]

case_mapping = {
    "ingo_morning": 1,
    "ingo_noon": 2,
    "ingo_evening": 3,
    "ingo_sensor": 4,
}

non_rl_model_names = ["maxpressure", "fixedtime"]

model_names = rl_model_names + non_rl_model_names

items = []

for case_name in case_names:
    for model_name in model_names:
        
        if model_name in rl_model_names:
            df = experiments[model_name][case_name]
            travel_time_series = df["travel_time"].iloc[1:]
            optimum_time = travel_time_series.min()
        elif model_name in non_rl_model_names and case_name in experiments[model_name].keys():
            df = experiments[model_name][case_name]
            optimum_time = travel_time_series = df["travel_time"].min()
        else:
            optimum_time = None

        item = {}
        item["model_name"] = model_name
        item["case"] = case_name
        item["optimum_travel_time"] = optimum_time

        items.append(item)

output_df = pd.DataFrame(items)
output_df["case"] = output_df["case"].map(case_mapping)

output_df = output_df.pivot(index="case", columns="model_name")['optimum_travel_time'].reindex(columns=model_names)

output_df.to_csv(OUTPUT_DIRECTORY + "final_travel_time.csv")



print("done")