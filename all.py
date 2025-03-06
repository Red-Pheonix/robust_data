import pandas as pd

# open csv file and load into pandas dataframe
GRID_FILE = "summary//grid4x4//all.csv"
INGO_FILE = "summary//ingo//all.csv"


grid_df = pd.read_csv(GRID_FILE)
ingo_df = pd.read_csv(INGO_FILE)

# grid data
grid_summary = (
    grid_df[["model_name", "recovery_time", "initial_drop"]]
    .groupby("model_name")
    .mean()
    .T.reindex(columns=["dqn", "mplight", "colight"])
)

ingo_summary = (
    ingo_df[["model_name", "recovery_time", "initial_drop"]]
    .groupby("model_name")
    .mean()
    .T.reindex(columns=["dqn", "colight"])
)

df = pd.concat([grid_summary, ingo_summary], keys=['grid','ingo']).T

recovery_df = df.loc[:, df.columns.get_level_values(1) == 'recovery_time'].T
initial_df = df.loc[:, df.columns.get_level_values(1) == 'initial_drop'].T

recovery_df.to_csv("summary//recovery_time.csv")
initial_df.to_csv("summary//initial_drop.csv")

print("test")
