import json
import logging
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm

import configuration as cfg
from environment.routing_simulator import RoutingSimulator
from metrics import RoutingAlgorithmMetrics


def run():
    args = setup_parser()
    if args.show_plots:
        setattr(cfg, 'show_plots', True)

    # global logger
    logging.basicConfig(format='%(asctime)s INFO: %(message)s', level=logging.INFO)

    with open('scenario.json', 'r') as scenario_file:
        data = json.load(scenario_file)

        for scenario_name in data.keys():
            try:
                run_scenario(data[scenario_name], scenario_name)
            except NotImplementedError:
                return


def setup_parser():
    parser = argparse.ArgumentParser(description='Simulation options.')
    parser.add_argument('--show_plots', action='store_true', help='Switch for showing plots.')
    return parser.parse_args()


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


def run_scenario(scenario: dict[str], scenario_name: str):
    if not validate_scenario(scenario):
        raise NotImplementedError

    setattr(cfg, 'target_field_x_axis', scenario["x_axis_bounds"])
    setattr(cfg, 'target_field_y_axis', scenario["y_axis_bounds"])

    logging.info(f'Starting simulation for scenario: {scenario_name}')
    # create directories for logs and results
    Path("./logs").mkdir(parents=True, exist_ok=True)
    Path("./results").mkdir(parents=True, exist_ok=True)

    simulation_logger = setup_logger(f'{scenario_name}_logger', f'./logs/scenario-{scenario_name}.log')
    simulation_metrics = list()
    env = RoutingSimulator(
        num_of_nodes=scenario['num_of_nodes'],
        initial_node_energy=scenario['initial_node_energy'],
        simulation_logger=simulation_logger,
        bs_location=scenario['base_station_location'],
        max_rounds=scenario["max_rounds"] if "max_rounds" in scenario else None
    )

    for algorithm in scenario['algorithms']:
        if algorithm in cfg.supported_algorithms:
            simulation_logger.info(f'Starting simulation for {algorithm}')
            metric: RoutingAlgorithmMetrics = env.simulate(cfg.supported_algorithms[algorithm], simulation_logger)
            env.energy_metrics = RoutingAlgorithmMetrics()
            simulation_metrics.append(metric)

    # plotting metrics
    for scenario_metric in scenario['metrics']:
        if scenario_metric == 'received_packets':
            algorithm_names = [metric.algorithm_name for metric in simulation_metrics]
            received_packets = [metric.received_packets for metric in simulation_metrics]
            y_bottom_lim = min(received_packets)-0.05*min(received_packets)
            y_upper_lim = max(received_packets)+0.05*max(received_packets)
            plt.ylim(y_bottom_lim, y_upper_lim)
            plt.bar(algorithm_names, received_packets)
            plt.title(cfg.metrics_plot_configuration[scenario_metric]['title'])

            plt.ylabel(cfg.metrics_plot_configuration[scenario_metric]['label'])
            plt.savefig(f'./results/received_packets.png', dpi=400)
            if cfg.show_plots:
                plt.show()
            plt.clf()
            continue

        if scenario_metric == 'first_dead_node':
            algorithm_names = [metric.algorithm_name for metric in simulation_metrics]
            first_dead_node = [metric.first_dead_node for metric in simulation_metrics]
            y_bottom_lim = min(first_dead_node)-0.05*min(first_dead_node)
            y_upper_lim = max(first_dead_node)+0.05*max(first_dead_node)
            plt.ylim(y_bottom_lim, y_upper_lim)
            plt.bar(algorithm_names, first_dead_node)
            plt.title(cfg.metrics_plot_configuration[scenario_metric]['title'])
            plt.ylabel(cfg.metrics_plot_configuration[scenario_metric]['label'])
            plt.savefig(f'./results/first_dead_node.png', dpi=400)
            if cfg.show_plots:
                plt.show()
            plt.clf()
            continue

        if scenario_metric == 'total_energy_dissipation':
            algorithm_names = [metric.algorithm_name for metric in simulation_metrics]
            total_energy_dissipation = [metric.total_energy_dissipation_200 for metric in simulation_metrics]
            y_bottom_lim = min(total_energy_dissipation) - 0.05*min(total_energy_dissipation)
            y_upper_lim = max(total_energy_dissipation) + 0.05*max(total_energy_dissipation)
            plt.ylim(y_bottom_lim, y_upper_lim)
            plt.bar(algorithm_names, total_energy_dissipation)
            plt.title(cfg.metrics_plot_configuration[scenario_metric]['title'])
            plt.ylabel(cfg.metrics_plot_configuration[scenario_metric]['label'])
            plt.savefig(f'./results/total_energy_dissipation.png', dpi=400)
            if cfg.show_plots:
                plt.show()
            plt.clf()
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
            if cfg.show_plots:
                plt.show()
            plt.clf()

    return simulation_metrics


def validate_scenario(scenario: dict[str]) -> bool:
    if "num_of_nodes" not in scenario:
        logging.error("num_of_nodes parameter not given in the scenario")
        return False

    if "initial_node_energy" not in scenario:
        logging.error("initial_node_energy parameter not given in the scenario")
        return False

    for algorithm in scenario['algorithms']:
        if algorithm not in cfg.supported_algorithms:
            logging.error("Routing algorithm defined in scenario is not supported")
            return False

    if len(scenario["algorithms"]) == 0:
        logging.error("empty algorithms parameter in the scenario")
        return False

    for metric in scenario['metrics']:
        if metric not in cfg.supported_metrics:
            logging.error("Metric defined in scenario is not supported")
            return False

    if len(scenario["metrics"]) == 0:
        logging.error("empty metrics parameter in the scenario")
        return False

    if scenario["num_of_nodes"] > 1000 or scenario["num_of_nodes"] <= 0:
        logging.error("Invalid num_of_nodes number")
        return False

    if scenario["initial_node_energy"] > 5 or scenario["initial_node_energy"] < 0.1:
        logging.error("Invalid initial_node_energy number")
        return False

    if "base_station_location" not in scenario:
        logging.error("base_station_location parameter not given in the scenario")
        return False

    if "bits_per_message" not in scenario:
        logging.error("bits_per_message parameter not given in the scenario")
        return False

    if scenario["bits_per_message"] < 100 or scenario["bits_per_message"] > 10000:
        logging.error("invalid value for bits_per_message parameter")
        return False

    if "x_axis_bounds" not in scenario:
        logging.error("x_axis_bounds parameter not given in the scenario")
        return False

    if "y_axis_bounds" not in scenario:
        logging.error("y_axis_bounds parameter not given in the scenario")
        return False

    if ("Leach" or "LeachC" in scenario["algorithms"]) and "desired_clusters_percentage" not in scenario:
        logging.error("desired_clusters_percentage parameter must be provided in the scenario")
        return False

    if scenario["desired_clusters_percentage"] < 1 or scenario["desired_clusters_percentage"] > 90:
        logging.error("invalid value for desired_clusters_percentage parameter")
        return False

    if "max_rounds" in scenario and scenario["max_rounds"] < 1:
        logging.error("invalid value for max_rounds parameter")
        return False

    if "radio_propagation_model" not in scenario:
        logging.error("radio_propagation_model parameter not given in the scenario")
        return False

    if scenario["radio_propagation_model"] not in cfg.supported_radio_propagation_models:
        logging.error("radio propagation model defined in scenario is not supported.")
        return False

    return True


if __name__ == "__main__":
    run()

