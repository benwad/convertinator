import pint
ureg = pint.UnitRegistry()


def convert_to_metric(quantity, from_unit, to_unit):
    original = float(quantity) * ureg(from_unit)
    converted = original.to(to_unit).to_tuple()
    return converted[0], converted[1][0][0]


def convert_to_celsius(quantity, from_unit, to_unit):
    original = ureg.Quantity(float(quantity), ureg(from_unit))
    converted = original.to(to_unit).to_tuple()
    return converted[0], converted[1][0][0]


units = [
    {
        'regex': r'([0-9.]+) (acres?)',
        'from_unit': 'acres',
        'to_unit': 'square kilometers',
        'convert_function': convert_to_metric,
        'from_symbol': 'acres',
        'to_symbol': 'km^2'
    },
    {
        'regex': r'([0-9.]+) (miles?)',
        'from_unit': 'miles',
        'to_unit': 'kilometers',
        'convert_function': convert_to_metric,
        'from_symbol': 'miles',
        'to_symbol': 'km'
    },
    {
        'regex': r'([0-9.]+) (ft)',
        'from_unit': 'feet',
        'to_unit': 'metres',
        'convert_function': convert_to_metric,
        'from_symbol': 'ft',
        'to_symbol': 'metres'
    },
    {
        'regex': r'([0-9.]+) (foot)',
        'from_unit': 'feet',
        'to_unit': 'metres',
        'convert_function': convert_to_metric,
        'from_symbol': 'ft',
        'to_symbol': 'metres'
    },
    {
        'regex': r'([0-9.]+) (feet)',
        'from_unit': 'feet',
        'to_unit': 'metres',
        'convert_function': convert_to_metric,
        'from_symbol': 'ft',
        'to_symbol': 'metres'
    },
    {
        'regex': r'([0-9.]+) (pounds)',
        'from_unit': 'lb',
        'to_unit': 'kg',
        'convert_function': convert_to_metric,
        'from_symbol': 'lb',
        'to_symbol': 'kg',
    },
    {
        'regex': r'([0-9.]+) (lb)',
        'from_unit': 'lb',
        'to_unit': 'kg',
        'convert_function': convert_to_metric,
        'from_symbol': 'lb',
        'to_symbol': 'kg',
    },
    {
        'regex': r'([0-9.]+) (oz)',
        'from_unit': 'ounces',
        'to_unit': 'grams',
        'convert_function': convert_to_metric,
        'from_symbol': 'ounces',
        'to_symbol': 'grams',
    },
    {
        'regex': r'([0-9.]+) (ounces)',
        'from_unit': 'ounces',
        'to_unit': 'grams',
        'convert_function': convert_to_metric,
        'from_symbol': 'ounces',
        'to_symbol': 'grams',
    },
    {
        'regex': r'(-?[0-9.]+) (degrees farenheit)',
        'from_unit': 'degF',
        'to_unit': 'degC',
        'convert_function': convert_to_celsius,
        'from_symbol': '°F',
        'to_symbol': '°C'
    },
    {
        'regex': r'(-?[0-9.]+) (farenheit)',
        'from_unit': 'degF',
        'to_unit': 'degC',
        'convert_function': convert_to_celsius,
        'from_symbol': '°F',
        'to_symbol': '°C'
    },
    {
        'regex': r'(-?[0-9.]+)(F)',
        'from_unit': 'degF',
        'to_unit': 'degC',
        'convert_function': convert_to_celsius,
        'from_symbol': '°F',
        'to_symbol': '°C'
    },
]
