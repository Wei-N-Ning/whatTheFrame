
import inspect
import re
import types


class COMPLEXTYPE(object):
    pass


class VarDeepInspect(object):
    """
    Given a Python object, inspects its state via its __dict__ attribute if it has one;
    Recursively looks into its attributes and returns a nested dictionary.
    """

    primitive_types = {int, float, bool, basestring, types.NoneType}

    def __init__(self):
        # to avoid circular reference
        self._visited_ids = set()

    def __call__(self, var):
        o_dict = dict()
        try:
            ret = self.inspect(var, o_dict)
        except Exception, e:
            return o_dict
        if ret is COMPLEXTYPE:
            return o_dict
        return ret

    def inspect(self, var, o_dict):
        """
        if the given object is a standard Python container type or possess __dict__ attributes,
        recurse into its elements or attributes
        Args:
            var:
            o_dict (dict):

        Returns:
            if the given object is of a primitive type, return its value;
            if the given object does not have a __dict__ attribute (such as FFI objects), return its string
                representation;
            for everything else return COMPLEXTYPE;
        """

        if isinstance(var, type):
            return str(var)

        T = type(var)

        if T in self.primitive_types:
            return var

        id_ = id(var)
        if id_ in self._visited_ids:
            return 'circular_reference:{}'.format(var)
        self._visited_ids.add(id_)

        if 'iteritems' in dir(T):
            type_name = getattr(T, '__name__', 'dict')
            return self.inspect_dict(var.iteritems(), o_dict, prefix='{}:'.format(type_name))

        if '__iter__' in dir(var) and not isinstance(var, types.FileType):
            type_name = getattr(T, '__name__', 'sequence')
            return self.inspect_dict(enumerate(var), o_dict, prefix='{}:'.format(type_name))

        if '__dict__' in dir(var):
            return self.inspect_dict(var.__dict__.iteritems(), o_dict, prefix='attr:')

        return str(var)

    def inspect_dict(self, item_iter, o_dict, prefix='key:'):
        if '__iter__' not in dir(item_iter):
            return str(item_iter)
        for k, v in item_iter:
            d = dict()
            r = self.inspect(v, d)
            nice_k = '{}{}'.format(prefix, k)
            if r is COMPLEXTYPE:
                o_dict[nice_k] = d
            else:
                o_dict[nice_k] = r
        return COMPLEXTYPE


class VarInspectorTemplate(object):
    """
    Template: a comma-separate list of attribute names and getter method names;
    Getter methods are expected to take no argument;

    """
    def __init__(self, template):
        self._attr_names = list()
        self._getter_names = list()
        for token in template.split(','):
            token = token.strip()
            if token.endswith('()'):
                self._getter_names.append(token.replace('()', ''))
            else:
                self._attr_names.append(token)

    def __call__(self, var):
        T = type(var)
        result = dict()
        type_name = getattr(T, '__name__', '')
        if type_name:
            result['type'] = type_name
        for attr_name in self._attr_names:
            try:
                attr_value = getattr(var, attr_name, '')
            except Exception, e:
                attr_value = repr(e)
            if attr_value:
                result[attr_name] = attr_value
        for getter_name in self._getter_names:
            meth = getattr(var, getter_name, None)
            if meth is not None:
                try:
                    v = meth()
                except Exception, e:
                    v = repr(e)
                result['{}()'.format(getter_name)] = VarDeepInspect()(v)
        return result


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

    _json_friendly_types = {int, float, bool, basestring}

    def __init__(self):
        self._filters = list()
        self._parser = FrameInspectorBase.default_parse
        self._inspector_by_type = dict()
        self._inspector_by_regex = dict()

    def register_inspector(self, type_, op):
        """

        Args:
            type_ (type):
            op (callable):

        Returns:

        """
        self._inspector_by_type[type_] = op

    def register_inspector_regex(self, type_regex, op):
        """

        Args:
            type_regex (str):
            op (callable):

        Returns:

        """
        self._inspector_by_regex[type_regex] = op

    def register_filter(self, fi):
        self._filters.append(fi)

    def register_parser(self, pa):
        self._parser = pa

    @staticmethod
    def default_parse(f):
        (filename, line_number, function_name, lines, index) = inspect.getframeinfo(f)
        return dict(filename=filename, line_number=line_number, function_name=function_name, lines=lines, index=index)

    def filter_frame(self, f):
        if not self._filters:
            return True
        for fi in self._filters:
            if not fi(f):
                return False
        return True

    def inspect_var(self, var):
        T = type(var)
        full_type_name = str(type(var))
        _ = re.search('\'(.+)\'', str(type(var)))
        if _ is not None:
            full_type_name = _.groups()[0]
        op = self._inspector_by_type.get(T, None)
        if op is None:
            for regex, _ in self._inspector_by_regex.iteritems():
                if re.match(regex, full_type_name) is not None:
                    op = _
                    break
        if op is None:
            op = VarDeepInspect()
        return op(var)

    def inspect(self, f):
        """

        Args:
            f (types.FrameType):

        Returns:
            dict:
        """
        result = dict()
        if not self.filter_frame(f):
            return result
        result.update(self._parser(f))
        variables = dict()
        for name, value in f.f_locals.iteritems():
            serialized_value = self.inspect_var(value)
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

    def __init__(self, tb):
        self._tb = tb

    def __iter__(self):
        f = self._tb.tb_frame
        while f:
            yield f
            f = f.f_back
