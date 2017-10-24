
import unittest
from pprint import pprint as pp

from whatTheFrame import deepInspect


class TestDeepInspect(unittest.TestCase):

    def setUp(self):
        self.op = deepInspect.DeepInspect()

    def test_containerTypes(self):
        result = self.op.do([1, {'a': 33.34}])
        self.assertEqual({'list:0': 1, 'list:1': {'dict:a': 33.34}}, result)

    def test_classInstances(self):
        """
        {'set:0': {'attr:a': {'list:0': 1.03, 'list:1': 0.2, 'list:2': -2},
           'attr:b': {'attr:a': None, 'attr:b': 2}},
         'set:1': {'attr:a': 'something', 'attr:b': {'dict:make_it_harder': True}}}
        """
        class A(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b
        result = self.op.do((A('something', {'make_it_harder': True}), A([1.03, 2e-1, -0x2], A(None, 2))))
        self.assertEqual(
            {'attr:a': 'something', 'attr:b': {'dict:make_it_harder': True}}, result['tuple:0'])

