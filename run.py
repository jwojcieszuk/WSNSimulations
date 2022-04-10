import json
import logging

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

import configuration as cfg
from environment.routing_simulator import RoutingSimulator
from metrics import RoutingAlgorithmMetrics


def run():
    with open('scenario.json', 'r') as scenario_file:
        data = json.load(scenario_file)

        for scenario_name in data.keys():
            run_scenario(data[scenario_name], scenario_name)


def setup_logger(name, log_file, level=logging.DEBUG):
    handler = logging.FileHandler(log_file, mode='w')
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def run_scenario(scenario, scenario_name):
    simulation_logger = setup_logger(f'{scenario_name}_logger', f'./logs/scenario-{scenario_name}.log')
    simulation_metrics = list()
    env = RoutingSimulator(
        num_of_nodes=scenario['num_of_nodes'],
        initial_node_energy=scenario['initial_node_energy']
    )

    for algorithm in scenario['algorithms']:
        if algorithm in cfg.supported_algorithms:
            simulation_logger.info(f'Starting simulation for {algorithm}')
            metric: RoutingAlgorithmMetrics = env.simulate(cfg.supported_algorithms[algorithm], simulation_logger)
            simulation_metrics.append(metric)

    if not simulation_metrics:
        logging.info("Couldn't find any supported routing algorithms defined in scenario")
        return

    # plotting metrics
    for scenario_metric in scenario['metrics']:
        if scenario_metric == 'received_packets':
            algorithm_names = [metric.algorithm_name for metric in simulation_metrics]
            received_packets = [metric.received_packets for metric in simulation_metrics]
            plt.bar(algorithm_names, received_packets)
            plt.title(cfg.metrics_plot_configuration[scenario_metric]['title'])
            plt.ylabel(cfg.metrics_plot_configuration[scenario_metric]['label'])
            plt.savefig(f'./results/received_packets.png', dpi=400)
            plt.show()
            continue

        if scenario_metric in cfg.supported_metrics:
            color = iter(cm.rainbow(np.linspace(0, 1, len(simulation_metrics))))
            for simulation_metric in simulation_metrics:
                metric = simulation_metric.__getattribute__(scenario_metric)
                plt.plot(
                    simulation_metric.rounds_num,
                    metric,
                    color=next(color),
                    label=simulation_metric.algorithm_name
                )

            plt.title(cfg.metrics_plot_configuration[scenario_metric]['title'])
            plt.ylabel(cfg.metrics_plot_configuration[scenario_metric]['label'])
            plt.xlabel('Rounds')
            plt.legend(loc=cfg.metrics_plot_configuration[scenario_metric]['legend_location'])
            plt.savefig(f'./results/{scenario_metric}.png', dpi=400)
            plt.show()


if __name__ == "__main__":
    run()

