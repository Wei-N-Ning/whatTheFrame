
import inspect


class FrameInspectorBase(object):
    """
    An extension of inspect.getframeinfo(f), allowing client code to extend this base class by registering their own
    operator(s)

    There 3 three types of operators:

    Filter: whether to handle this frame based on the name of the source module, the name of the function etc.
        there can be multiple filters
    InfoParser: transform the result of getframeinfo()
        there can be at most one parser
    VarSerializer: to handle specific type(s) of variable, converting their values to some json-serializable types
        there can be multiple serializer (one per type)

    The result is a Python dict that can be serialized to a json string.
    """

    _json_friendly_types = {int, float, bool, tuple, dict, list}

    def __init__(self):
        self._filters = list()
        self._parser = FrameInspectorBase._default_parse
        self._var_serializers = dict()

    def register_serializer(self, type_, op):
        self._var_serializers[type_] = op

    def register_filter(self, fi):
        self._filters.append(fi)

    def register_parser(self, pa):
        self._parser = pa

    @staticmethod
    def _default_parse(f):
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(f)
        return dict(filename=filename, line_number=line_number, function_name=function_name, lines=lines, index=index)

    @classmethod
    def _default_serializer(cls, var):
        if type(var) in cls._json_friendly_types:
            return var
        return str(var)

    def _filter_frame(self, f):
        if not self._filters:
            return True
        for fi in self._filters:
            if not fi(f):
                return False
        return True

    def inspect(self, f):
        """

        Args:
            f (types.FrameType):

        Returns:
            dict:
        """
        result = dict()
        if not self._filter_frame(f):
            return result
        result.update(self._parser(f))
        variables = dict()
        for name, value in f.f_locals.iteritems():
            op = self._var_serializers.get(type(value), self._default_serializer)
            serialized_value = op(value)
            variables[name] = serialized_value
        result['variables'] = variables
        return result


class FrameIterI(object):
    """
    Iterates over a number of Python frames (types.FrameType).
    The order of these frames is implementation-specific.
    Also each implementer may choose specific rules to limit the traversal.
    """

    def __iter__(self):
        """

        Yields:
            types.FrameType:
        """
        return iter(tuple())


class ReverseFromCurrentFrame(FrameIterI):

    def __init__(self, start_distance=2, max_distance=-1):
        """

        Args:
            start_distance (int): the magic number 2 is chosen as the default value so that the traversal by default
                                  starts at the closest caller from the function or method where this iterator is rolled
            max_distance (int): optional, to stop traversing if the distance is too far away from the current call
                                frame; use -1 to turn this limit off
        """
        self._start_distance = start_distance
        self._max_distance = max_distance

    def _should_stop(self, distance):
        if self._max_distance > 0:
            if distance > self._max_distance:
                return True
        return False

    @staticmethod
    def _iterate():
        f = inspect.currentframe()
        distance = 0
        while f:
            yield distance, f
            f = f.f_back
            distance += 1

    def __iter__(self):
        for distance, f in self._iterate():
            if self._should_stop(distance):
                break
            if distance < self._start_distance:
                continue
            yield f


class ReverseFromTB(FrameIterI):
    pass
