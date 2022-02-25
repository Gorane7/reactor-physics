from value import Value


class Particle:
    def __init__(self, symbol, mass_excess, name):
        self.symbol = symbol
        self.mass_excess = Value(mass_excess, "keV")
        self.name = name
        self.mass = None
        self.atom_number = None

    def calc_mass(self):
        atom_number = self.calc_atom_number()
        self.mass = Value(atom_number, "dalton").convert("keV")
        self.mass = self.mass.add(self.mass_excess)
        return self.mass

    def calc_atom_number(self):
        state = 0
        number = ""
        for letter in self.symbol:
            if state == 0:
                if letter.isalpha():
                    state = 1
            elif state == 1:
                if letter.isnumeric():
                    state = 2
                    number += letter
            else:
                number += letter
        self.atom_number = int(number)
        return self.atom_number
