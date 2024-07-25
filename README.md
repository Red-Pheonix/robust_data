# Introduction

This repo contains the raw data found from running experiments and the code for analysis for analyzing the robustness of ATSC-RL systems. A slightly modified version of [LibSignal](https://github.com/DaRL-LibSignal/LibSignal) was used as a testbed for the experiments. The details of how the experiment was run is explained in the [Modified LibSignal](https://github.com/Red-Pheonix/LibSignal/tree/robust_test_1) repo. Two scenarios were tested here: [Grid 4x4 Scenario](https://github.com/Red-Pheonix/Grid-4x4-Scenario) and [Ingolstadt Scenario](https://github.com/Red-Pheonix/sumo_ingolstadt).

## Case Result Files
The raw data from the experiments can be found in `grid4x4` and `ingo` folders. The data is divided into models and cases folderwise. The `summary` folder contains data regarding recovery time.

## Making graphs
The graphs for the Grid 4x4 scenario is found in `grid.ipynb` and `grid_2.ipynb` and for the Ingolstadt scenario is found in `ingo.ipynb` and `ingo_2.ipynb`. The `make_summary.py` script was used for making the data in the summary folder.