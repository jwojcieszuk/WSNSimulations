import configuration as cfg
import logging


class EnergySource(object):
    def __init__(self, parent, energy):
        self.energy = energy
        self.node = parent

    def recharge(self, energy):
        self.energy = energy


class Battery(EnergySource):
    def consume(self, energy):
        if self.energy >= energy:
            self.energy -= energy
        if self.energy == 0:
            self.node.battery_dead()


class PluggedIn(EnergySource):
    def consume(self, energy):
        pass
