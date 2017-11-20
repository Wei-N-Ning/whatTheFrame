
import json
from pprint import pprint as pp
import unittest

import mock

import whatTheFrame

from aCompany import gloryApp


def func(*args, **kwargs):
    frame_info = inspect_call_chain()
    store_frame_info(frame_info)

    # compute stuffs...
    pass


class Stateful(object):

    def __init__(self):
        self.a = [1, 2]
        self.b = {'a': 1, 'b': 2}

    def do(self):
        self.a.append(8)
        ins = whatTheFrame.FrameInspectorBase()
        f = iter(whatTheFrame.ReverseFromCurrentFrame(start_distance=2, max_distance=2)).next()
        result = ins.inspect(f)
        variables = result['variables']
        assert 'self' in variables
        s = variables['self']
        assert 'attr:a' in s


def inspect_call_chain():
    ins = whatTheFrame.FrameInspectorBase()
    frame_info = list()
    for f in whatTheFrame.ReverseFromCurrentFrame(start_distance=3):
        frame_info.append(ins.inspect(f))
    return frame_info


def store_frame_info(frame_info):
    with open('/tmp/out.json', 'w') as fp:
        json.dump(frame_info, fp)


class TestInspectCallChain(unittest.TestCase):

    def setUp(self):
        self.patcher = mock.patch('aCompany.gloryLib.winningApi.noFreedom.suicideCore.this_is_critical', func)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_retrieveFrameInfo_expectFrameDetails(self):
        gloryApp.run()
        with open('/tmp/out.json', 'r') as fp:
            frame_info = json.load(fp)
        f = frame_info[0]
        self.assertEqual(f['function_name'], 'func', msg=f['function_name'])
        self.assertEqual(len(frame_info), 5, msg=str(len(frame_info)))


class TestRetrieveStateInformation(unittest.TestCase):

    def test_(self):
        sta = Stateful()
        sta.do()
