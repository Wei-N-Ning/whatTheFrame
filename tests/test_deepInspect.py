
import unittest
from pprint import pprint as pp

from whatTheFrame import DeepInspect


class A(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b


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

