import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import PercentFormatter

DIRECTORY = "ingo"

def plot_df(timestep_df, timestep, model_name, case_name):

    fig = plt.figure(figsize=(8, 6))
    
    plt.hist(timestep_df['queueing_length'],
            bins=[0, 1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000],
            alpha=0.75,
            color='skyblue',
            edgecolor='black',
            linewidth=2,
            density=True
    )


    plt.title(f'Queue Length Histogram - {model_name}', fontweight='bold', fontsize=20)
    plt.xlabel("Queueing Length", fontsize=16)
    plt.ylabel('Percantage of Roads', fontsize=16)
    plt.grid(True, alpha=0.2)

    plt.xscale('log')
    plt.xticks([0.1,1,10,100,1000], fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(0, 1.0)

    plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=1))

    plt.gca().set_facecolor('whitesmoke')
    
    # 
    output_dir = os.path.join(DIRECTORY, model_name, case_name, "distributions")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f'{case_name}_dist_{timestep}.png')
    fig.savefig(filename, dpi=300, facecolor='white')
    
    plt.close()

all_files = glob.glob(os.path.join(DIRECTORY, '**', '*queue.csv'), recursive=True)
all_files.sort()


experiments = {}
experiments['colight'] = {}
experiments['dqn'] = {}
experiments['mplight'] = {}
experiments['fixedtime'] = {}
experiments['maxpressure'] = {}

for filename in all_files:
    model_name = filename.split("/")[1]
    experiment_name = filename.split("/")[-1].rstrip(".csv")
    df = pd.read_csv(filename)
    experiments[model_name][experiment_name] = df


for model_name, model_experiments in experiments.items():
    for experiment_name, experiment_df in model_experiments.items():
        for timestep, timestep_df in experiment_df.groupby("timestep"):
            case_name = experiment_name.rstrip("_queue")
            print(f"Plotting {model_name} - {case_name} - {timestep}")
            plot_df(timestep_df, str(timestep-360), model_name, case_name)

