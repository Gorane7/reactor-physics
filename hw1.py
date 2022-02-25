from reaction import Reaction
from value import Value
from data import c
from conversions import conversions
import math
import matplotlib.pyplot as plt


class Main:
    def __init__(self):
        pass

    def run(self):
        [(task(), print()) for task in [self.task1, self.task2, self.task3, self.task5]]

    def task1(self):
        # Subtask 1
        print(f'Q value for reaction 1: {Reaction(["1H2", "1H3"], ["2He4", "0n1"]).calc_q_value()}')

        # Subtask 2
        reaction2_a = Reaction(["1H2", "1H2"], ["1H3", "1H1"])
        reaction2_b = Reaction(["1H2", "1H2"], ["2He3", "0n1"])
        print(f"Q1 value for reaction 2: {reaction2_a.calc_q_value()}")
        print(f"Q2 value for reaction 2: {reaction2_b.calc_q_value()}")
        print(f"Total Q value for reaction 2: {reaction2_a.calc_q_value().add(reaction2_b.calc_q_value()).divide(2)}")

    def task2(self):
        # Subtask 2
        fission_reaction = Reaction(["92U235", "0n1"])
        fission_reaction.set_q_value(Value(179 + 8 + 2 + 4, "MeV"))
        fission_reaction.calc_input_mass()

        fusion_reaction_1 = Reaction(["1H2", "1H3"], ["2He4", "0n1"])
        fusion_reaction_2 = Reaction(["1H2", "1H2"], ["1H3", "1H1"])

        print(f"Percent of mass converted to energy in fission reactions {fission_reaction.calc_energy_conversion_coefficient().convert('%').raw_string()}")
        print(f"Percent of mass converted to energy in fusion reaction 1: {fusion_reaction_1.calc_energy_conversion_coefficient().convert('%').raw_string()}")
        print(f"Percent of mass converted to energy in fusion reaction 2: {fusion_reaction_2.calc_energy_conversion_coefficient().convert('%').raw_string()}")

        # BWRX-300 RPV dimensions, based on https://aris.iaea.org/PDF/BWRX-300_2020.pdf
        height_1 = 26
        diameter_1 = 4
        volume_1 = math.pi * (diameter_1 / 2)**2 * height_1
        energy_production_1 = 300  # in MW
        energy_per_volume_1 = energy_production_1 * 1000 / volume_1  # in kW

        # ITER volume and heat energy production, based on https://www.iter.org/FactsFigures
        volume_2 = 830
        energy_production_2 = 500  # in MW
        energy_per_volume_2 = energy_production_2 * 1000 / volume_2

        print(f"BWRX-300 energy per volume: {energy_per_volume_1} kW/m^3")
        print(f"ITER energy per volume: {energy_per_volume_2} kW/m^3")

    def task3(self):
        power_per_reaction = Value(179 + 8 + 2 + 4, "MeV").convert("J").convert("GJ")
        power_per_second_needed = Value(3, "GJ")
        reactions_per_second = power_per_second_needed.divide(power_per_reaction)
        print(f"Fission reactions per second needed: {reactions_per_second}")

        power_needed = power_per_second_needed.convert("J").multiply(3600).multiply(24).multiply(365.25)
        mass_needed = power_needed.divide(c.value).divide(c.value)  # TODO: remove ugly hack, needs more detailed unit system
        mass_needed.unit = "kg"
        print(f"{mass_needed} of mass gets converted to energy per year.")

    @staticmethod
    def P(T, pi, k, e, E):
        frac = 2 * pi / ((pi * k * T)**1.5)
        frac_E = frac * math.sqrt(E)
        power = -E / (k * T)
        e_p = e**power
        return frac_E * e_p

    def task5(self):
        pi = math.pi
        k = 1.3806 * 10 ** (-23)
        e = math.e
        j_to_ev = 6.242 * 10**18
        max_e = 5 * 10**(-20)
        steps = 100
        step = max_e / steps
        values_300 = []
        values_600 = []
        values_ev = []
        for i in range(steps + 1):
            values_300.append(Main.P(300, pi, k, e, i * step))
            values_600.append(Main.P(600, pi, k, e, i * step))
            values_ev.append(i * step * j_to_ev)
        total_300 = sum(values_300)
        total_600 = sum(values_600)

        values_300 = [steps * x / total_300 / values_ev[-1] for x in values_300]
        values_600 = [steps * x / total_600 / values_ev[-1] for x in values_600]

        total_300 = sum(values_300)
        total_600 = sum(values_600)
        sum_300 = 0
        for i, value in enumerate(values_300):
            sum_300 += value
            if sum_300 * 2 >= total_300:
                ev_300 = values_ev[i]
                i_300 = i
                break
        sum_600 = 0
        for i, value in enumerate(values_600):
            sum_600 += value
            if sum_600 * 2 >= total_600:
                ev_600 = values_ev[i]
                i_600 = i
                break

        plt.plot(values_ev, values_300, color="b")
        plt.plot(values_ev, values_600, color="orange")
        plt.xlabel("E (eV)")
        plt.ylabel("Xp (1/eV)")
        print(f"Mean energy for a 300 K neutron is {ev_300} eV and for a 600 K neutron, it is {ev_600} eV.")
        plt.vlines([ev_300], ymin=0, ymax=values_300[i_300], color="b")
        plt.vlines([ev_600], ymin=0, ymax=values_600[i_600], color="orange")
        # plt.show()

        speeds_300 = [math.sqrt(2 * x * conversions["MeV"]["J"] / 10**6 / (1.6749275 * 10**(-27))) for x in values_300]
        print(speeds_300)


if __name__ == '__main__':
    main = Main()
    main.run()
