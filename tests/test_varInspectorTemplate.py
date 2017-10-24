
import unittest

from whatTheFrame import VarInspectorTemplate


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


class TestInspectorTemplate(unittest.TestCase):

    def test_expandAttrNames(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = VarInspectorTemplate('a,b,c,d')
        self.assertEqual({'a': [1, 2], 'b': {'make_it_harder': [True, True]}, 'type': 'A'}, op(a))

    def test_expandAttrNames_expectExceptionCaught(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = VarInspectorTemplate('e,c,d')
        result = op(a)
        self.assertEqual({'e': "RuntimeError('by designed',)", 'type': 'A'}, result)

    def test_expandGetterNames(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = VarInspectorTemplate('c,get_properties()')
        result = op(a)
        expected_result = {'get_properties()': {'dict:a': {'list:0': 1, 'list:1': 2},
                           'dict:b': {'dict:make_it_harder': {'list:0': True,
                                                              'list:1': True}}},
                           'type': 'A'}
        self.assertEqual(expected_result, result)

    def test_expandGetterNames_expectExceptionCaught(self):
        a = A([1, 2], {'make_it_harder': [True, True]})
        op = VarInspectorTemplate('throw()')
        result = op(a)
        self.assertEqual({'throw()': "RuntimeError('by designed',)", 'type': 'A'}, result)

