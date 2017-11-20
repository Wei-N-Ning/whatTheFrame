
from pprint import pprint as pp
import unittest

from whatTheFrame import FrameInspectorBase


class B(dict):
    """"""


class ABoom(dict):
    """"""


class TestFrameInspectorBase(unittest.TestCase):

    def setUp(self):
        self.op = FrameInspectorBase()

    def test_registerPerTypeInspector_expectValue(self):
        def inspect(var):
            return {'custom': '++'}
        self.op.register_inspector(B, inspect)
        b = B(p=1, q=2)
        result = self.op.inspect_var(b)
        self.assertEqual({'custom': '++'}, result)

    def test_registerInspectorByRegex_expectFailToMatch(self):
        def inspect(var):
            return {'custom': '++'}
        self.op.register_inspector_regex('AB\w+', inspect)
        b = ABoom(a=1, b=2)
        result1 = self.op.inspect_var(b)
        self.assertEqual({'ABoom:a': 1, 'ABoom:b': 2}, result1)

    def test_registerInspectorByRegex_mustUseFullTypeName(self):
        def inspect(var):
            return {'custom': '++'}
        self.op.register_inspector_regex('.+AB\w+', inspect)
        b = B(a=1, b=2)
        result1 = self.op.inspect_var(b)
        self.assertEqual({'B:a': 1, 'B:b': 2}, result1)
        ab = ABoom(c=1, d=2)
        result2 = self.op.inspect_var(ab)
        self.assertEqual({'custom': '++'}, result2)

