
import re


def convert_anything_to_float(anything):
    if anything is None:
        return 0.0
    if isinstance(anything, float):
        return anything
    if isinstance(anything, (int, bool)):
        return float(anything)
    if isinstance(anything, basestring) and re.search('[0-9.]{1, }', anything) is not None:
        return float(anything)
    try:
        return float(anything)
    except Exception, e:
        return 0.0


def convert_whatever_to_list(whatever):
    if not bool(whatever):
        return list()
    try:
        return list(whatever)
    except Exception, e:
        return [whatever]


def take_whatever_comes_first(whatever):
    aList = convert_whatever_to_list(whatever)
    if not aList:
        return None
    return aList[0]


def this_is_critical(value):
    if value <= 10:
        raise ValueError('OMG how can this ever happen????? Value: {}'.format(value))
    return convert_whatever_to_list(value)
