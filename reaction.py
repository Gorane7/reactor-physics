from data import particles
from value import Value
from functools import reduce


class Reaction:
    def __init__(self, inputs, outputs=None):
        self.inputs = [particles[x] for x in inputs]
        self.outputs = [particles[x] for x in outputs] if outputs is not None else None
        self.q_value = None
        self.input_mass = None
        self.energy_coefficient = None

    def calc_q_value(self):
        if self.outputs is None:
            raise Exception("Not enough information to calculate")
        in_value = reduce(lambda a, b: a.add(b), [x.mass_excess for x in self.inputs])
        out_value = reduce(lambda a, b: a.add(b), [x.mass_excess for x in self.outputs])
        self.q_value = in_value.subtract(out_value)
        return self.q_value

    def calc_input_mass(self):
        self.input_mass = reduce(lambda a, b: a.add(b), [x.calc_mass() for x in self.inputs])
        return self.input_mass

    def calc_energy_conversion_coefficient(self):
        input_mass = self.get_input_mass()
        q_value = self.get_q_value()
        self.energy_coefficient = q_value.divide(input_mass)
        return self.energy_coefficient

    def set_q_value(self, value):
        self.q_value = value

    def get_q_value(self):
        if self.q_value is None:
            return self.calc_q_value()
        return self.q_value

    def get_input_mass(self):
        if self.input_mass is None:
            return self.calc_input_mass()
        return self.input_mass

