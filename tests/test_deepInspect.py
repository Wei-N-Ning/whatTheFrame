
import collections
import unittest
from pprint import pprint as pp

from whatTheFrame import DeepInspect
from whatTheFrame import InspectorTemplate


class A(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_properties(self):
        return {'a': self.a, 'b': self.b}

    def throw(self):
        raise RuntimeError('by designed')

    @property
    def e(self):
        raise RuntimeError('by designed')


class TestDeepInspect(unittest.TestCase):

    def setUp(self):
        self.op = DeepInspect()

    def test_containerTypes(self):
        result = self.op([1, {'a': 33.34}])
        self.assertEqual({'list:0': 1, 'list:1': {'dict:a': 33.34}}, result)

    def test_classInstances(self):
        result = self.op((A('something', {'make_it_harder': True}), A([1.03, 2e-1, -0x2], A(None, 2))))
        self.assertEqual({'attr:a': 'something', 'attr:b': {'dict:make_it_harder': True}},
                         result['tuple:0'])

    def test_circularReference(self):
        a1 = A(None, None)
        a1.a = a1
        result = self.op(a1)
        self.assertTrue(result['attr:a'])

    def test_deepCircularReference(self):
        a1 = A(None, None)
        a2 = A(a1, None)
        a3 = A(a2, None)
        a1.b = a3
        result = self.op(a1)
        self.assertTrue(result['attr:b'])

    def test_orderedDict_expectTreatedAsDict(self):
        od = collections.OrderedDict(a=1, b=2)
        result = self.op(od)
        self.assertEqual({'OrderedDict:a': 1, 'OrderedDict:b': 2}, result)


class TestInspectorTemplate(unittest.TestCase):

    def test_expandAttrNames(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = InspectorTemplate('a,b,c,d')
        self.assertEqual({'a': [1, 2], 'b': {'make_it_harder': [True, True]}, 'type': 'A'}, op(a))

    def test_expandAttrNames_expectExceptionCaught(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = InspectorTemplate('e,c,d')
        result = op(a)
        self.assertEqual({'e': "RuntimeError('by designed',)", 'type': 'A'}, result)

    def test_expandGetterNames(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = InspectorTemplate('c,get_properties()')
        result = op(a)
        expected_result = {'get_properties()': {'dict:a': {'list:0': 1, 'list:1': 2},
                           'dict:b': {'dict:make_it_harder': {'list:0': True,
                                                              'list:1': True}}},
                           'type': 'A'}
        self.assertEqual(expected_result, result)

    def test_expandGetterNames_expectExceptionCaught(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = InspectorTemplate('throw()')
        result = op(a)
        self.assertEqual({'throw()': "RuntimeError('by designed',)", 'type': 'A'}, result)

