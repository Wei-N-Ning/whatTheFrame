
import collections
import types


class COMPLEXTYPE(object):
    pass


class DeepInspect(object):
    """
    Given a Python object, inspects its state via its __dict__ attribute if it has one;
    Recursively looks into its attributes and returns a nested dictionary.
    """

    primitive_types = {int, float, bool, basestring, types.NoneType}

    def do(self, var):
        o_dict = collections.OrderedDict()
        ret = self.inspect(var, o_dict)
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
            if the given object does not have a __dict__ attribute (such as FFI objects), return
                its string representation;
            for everything else return COMPLEXTYPE
        """

        T = type(var)

        if T in self.primitive_types:
            return var

        if T is dict:
            return self.inspect_dict(var.iteritems(), o_dict, prefix='dict:')

        if '__iter__' in dir(var):
            type_name = getattr(T, '__name__', 'sequence')
            return self.inspect_dict(enumerate(var), o_dict, prefix='{}:'.format(type_name))

        if '__dict__' in dir(var):
            return self.inspect_dict(var.__dict__.iteritems(), o_dict, prefix='attr:')

        return str(var)

    def inspect_dict(self, item_iter, o_dict, prefix='key:'):
        for k, v in item_iter:
            d = collections.OrderedDict()
            r = self.inspect(v, d)
            nice_k = '{}{}'.format(prefix, k)
            if r is COMPLEXTYPE:
                o_dict[nice_k] = d
            else:
                o_dict[nice_k] = r
        return COMPLEXTYPE
