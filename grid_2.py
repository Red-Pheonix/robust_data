import os
import glob
import matplotlib.pyplot as plt
import pandas as pd

DIRECTORY = "grid4x4"

all_files = glob.glob(os.path.join(DIRECTORY, "**", "*.csv"), recursive=True)
csv_files = [f for f in all_files if "queue" not in os.path.basename(f)]
csv_files.sort()


experiments = {}
experiments["colight"] = {}
experiments["dqn"] = {}
experiments["mplight"] = {}
experiments["fixedtime"] = {}
experiments["maxpressure"] = {}

for filename in csv_files:
    model_name = filename.split("/")[1]
    experiment_name = filename.split("/")[-1].rstrip(".csv")
    dqn_df = pd.read_csv(filename)
    experiments[model_name][experiment_name] = dqn_df


case_names = [
    "robust_morning_1",
    "robust_morning_2",
    "robust_morning_3",
    "robust_morning_4",
    "robust_morning_5",
    "robust_evening_1",
    "robust_pse_1",
    "robust_sensor",
]

rl_model_names = [
    "dqn",
    "colight",
    "mplight",
]

non_rl_model_names = ["maxpressure", "fixedtime"]

items = []
WINDOW = 3
THRESHOLD = 0.1

for case_name in case_names:
    for model_name in rl_model_names:
        df = experiments[model_name][case_name]
        travel_time_series = df["travel_time"].iloc[1:]
        initial_time = travel_time_series[1]
        # optimum_time = travel_time_series.nsmallest(3).mean()
        optimum_time = travel_time_series.min()
        threshold_times = (
            ((travel_time_series - optimum_time) / optimum_time)
            .rolling(WINDOW, min_periods=1)
            .apply(lambda x: (x < THRESHOLD).all())
            .astype(bool)
        )
        threshold_times.iloc[-1] = True
        recovery_time = threshold_times.idxmax()

        item = {}
        item["model_name"] = model_name
        item["case"] = case_name
        item["initial_travel_time"] = initial_time
        item["optimum_travel_time"] = optimum_time
        item["recovery_time"] = recovery_time

        items.append(item)

output_df = pd.DataFrame(items)
output_df["initial_drop"] = (
    (output_df["initial_travel_time"] - output_df["optimum_travel_time"])
    / output_df["initial_travel_time"]
    * 100
)
output_df = output_df.round(2)

OUTPUT_DIRECTORY = "summary/grid4x4/"

output_df.to_csv(OUTPUT_DIRECTORY + "all.csv", index=False)

output_df.groupby(["case"]).agg(
    {"initial_drop": "mean", "recovery_time": "mean"}
).transpose().round(2).to_csv(OUTPUT_DIRECTORY + "case.csv", index=False)

output_df.groupby(["model_name"]).agg(
    {"initial_drop": "mean", "recovery_time": "mean"}
).transpose().round(2).to_csv(OUTPUT_DIRECTORY + "model.csv", index=False)

for model_name in rl_model_names:
    df = output_df.groupby(["model_name", "case"]).sum().transpose()[model_name]
    df = df[case_names]
    df.to_csv(OUTPUT_DIRECTORY + model_name + ".csv", index=False)


