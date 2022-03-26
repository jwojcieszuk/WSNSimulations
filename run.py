import json
import logging

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

import configuration as cfg
from environment.environment import Environment
from metrics import RoutingAlgorithmMetrics


def run():
    logging.basicConfig(filename='simulator.log', filemode='w', encoding='utf-8', level=logging.INFO)
    simulation_metrics = list()

    with open('scenario.json', 'r') as scenario_file:
        data = json.load(scenario_file)
        env = Environment(num_of_nodes=data['num_of_nodes'])

        # gathering simulation results
        for algorithm in data['algorithms']:
            if algorithm in cfg.supported_algorithms:
                logging.info(f'Starting simulation for {algorithm}')
                metric: RoutingAlgorithmMetrics = env.simulate(cfg.supported_algorithms[algorithm])
                simulation_metrics.append(metric)

        if not simulation_metrics:
            logging.info("Couldn't find any supported routing algorithms defined in scenario")
            return

        # plotting metrics
        for scenario_metric in data['metrics']:
            if scenario_metric in cfg.supported_metrics:
                color = iter(cm.rainbow(np.linspace(0, 1, len(simulation_metrics))))

                for simulation_metric in simulation_metrics:
                    metric = simulation_metric.__getattribute__(scenario_metric)
                    plt.plot(
                        simulation_metric.rounds_num,
                        metric,
                        c=next(color),
                        label=simulation_metric.algorithm_name
                    )

                plt.ylabel(scenario_metric)
                plt.xlabel('Rounds')
                plt.legend(loc="lower left")
                plt.show()


if __name__ == "__main__":
    run()

