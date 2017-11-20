
import json
from pprint import pprint as pp
import sys
import unittest

import mock

import whatTheFrame

from aCompany import gloryApp


def throw(*args, **kwargs):
    try:
        # compute stuffs... and boom

        raise RuntimeError('')
    except RuntimeError, e:
        tb = sys.exc_traceback
        frame_info = inspect_exception(tb)
        store_frame_info(frame_info)


def inspect_exception(tb):
    ins = whatTheFrame.FrameInspectorBase()
    frame_info = list()
    for f in whatTheFrame.ReverseFromTB(tb):
        frame_info.append(ins.inspect(f))
    return frame_info


def store_frame_info(frame_info):
    with open('/tmp/out.json', 'w') as fp:
        json.dump(frame_info, fp)


class TestInspectException(unittest.TestCase):

    def setUp(self):
        self.patcher = mock.patch('aCompany.gloryLib.winningApi.noFreedom.suicideCore.this_is_critical', throw)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_retrieveFrameInfo_expectFrameDetails(self):
        gloryApp.run()


if __name__ == '__main__':
    unittest.main()
