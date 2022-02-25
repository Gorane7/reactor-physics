from conversions import conversions


class Value:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __str__(self):
        return self.string(2)

    def raw_string(self):
        return f"{self.value} {self.unit}"

    def string(self, round_precision=None):
        if round_precision is None:
            return f"{self.value} {self.unit}"
        return f"{round(self.value, round_precision)} {self.unit}"

    def add(self, other):
        if self.unit != other.unit:
            raise RuntimeError(f"Unable to convert between {self.unit} and {other.unit}")
        return Value(self.value + other.value, self.unit)

    def subtract(self, other):
        if self.unit != other.unit:
            raise RuntimeError(f"Unable to convert between {self.unit} and {other.unit}")
        return Value(self.value - other.value, self.unit)

    def divide(self, value):
        if not isinstance(value, Value):
            return Value(self.value / value, self.unit)
        value = value.convert(self.unit)
        return Value(self.value / value.value, "")

    def multiply(self, value):
        if not isinstance(value, Value):
            return Value(self.value * value, self.unit)
        raise RuntimeError("Confusing situation")

    def convert(self, target):
        if self.unit == target:
            return Value(self.value, self.unit)
        if self.unit not in conversions.keys():
            raise RuntimeError(f"Unable to convert {self.unit} to anything.")
        if target not in conversions[self.unit].keys():
            raise RuntimeError(f"Unable to convert {self.unit} to {target}.")
        return Value(self.value * conversions[self.unit][target], target)
