# Wireless Sensor Networks Simulator

This is a simulator for WSN written in Python 3.9. It supports communication from nodes to the Base Station(BS) with the use
of routing algorithms. Currently, it supports three algorithms - direct transmission to the Base Station, LEACH(Low-Energy Adaptive Clustering Hierarchy) and LEACH-centralized.


# How to run the program
Linux:
1. Install Python 3.9.
2. Open a terminal and inside the directory with the source code, create Python virtual environment with the command: `python3.9 -m venv ./venv`.
3. Activate the virtual environment with the command: `. ./venv/bin/activate`.
4. Install required modules with the command: `pip install -r requirements.txt`.
5. Run the program with the command `python3.9 run.py`.

Scenario file `scenario.json` can be modified or left with the default values.