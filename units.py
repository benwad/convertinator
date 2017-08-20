import re
import pint
ureg = pint.UnitRegistry()


class Converter(object):

    def __init__(self, regex, from_unit, to_unit, from_symbol, to_symbol):
        self.regex = re.compile(regex, re.MULTILINE)
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.from_symbol = from_symbol
        self.to_symbol = to_symbol

    def get_measurements(self, comment_body):
        measurements = []
        matches = self.regex.findall(comment_body)
        for match in matches:
            measurements.append((match[0], self))

        return measurements

    def convert_to_metric(self, quantity):
        raise NotImplementedError


class QuantityConverter(Converter):

    def convert_to_metric(self, quantity):
        original = float(quantity) * ureg(self.from_unit)
        converted = original.to(self.to_unit).to_tuple()
        return converted[0], converted[1][0][0]


class TemperatureConverter(Converter):

    def convert_to_metric(self, temperature):
        original = ureg.Quantity(float(temperature), ureg(self.from_unit))
        converted = original.to(self.to_unit).to_tuple()
        return converted[0], converted[1][0][0]


converters = [
    QuantityConverter(r'([0-9.]+) (acres?)', 'acres', 'square kilometers', 'acres', 'km^2'),
    QuantityConverter(r'([0-9.]+) (miles?)', 'miles', 'kilometers', 'miles', 'km'),
    QuantityConverter(r'([0-9.]+) (ft)', 'feet', 'metres', 'ft', 'metres'),
    QuantityConverter(r'([0-9.]+) (foot)', 'feet', 'metres', 'ft', 'metres'),
    QuantityConverter(r'([0-9.]+) (feet)', 'feet', 'metres', 'ft', 'metres'),
    QuantityConverter(r'([0-9.]+) (pounds)', 'lb', 'kg', 'lb', 'kg'),
    QuantityConverter(r'([0-9.]+) (lb)', 'lb', 'kg', 'lb', 'kg'),
    QuantityConverter(r'([0-9.]+) (oz)', 'ounces', 'grams', 'ounces', 'grams'),
    QuantityConverter(r'([0-9.]+) (ounces)', 'ounces', 'grams', 'ounces', 'grams'),
    TemperatureConverter(r'(-?[0-9.]+) (degrees farenheit)', 'degF', 'degC', '°F', '°C'),
    TemperatureConverter(r'(-?[0-9.]+) (farenheit)', 'degF', 'degC', '°F', '°C'),
    TemperatureConverter(r'(-?[0-9.]+)(F)', 'degF', 'degC', '°F', '°C'),
]
