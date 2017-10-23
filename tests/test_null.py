
from pprint import pprint as pp
import unittest

import whatTheFrame

from aCompany import gloryApp
from aCompany.gloryLib.winningApi.noFreedom import suicideCore


def func(*args, **kwargs):
    peek2()
    pass


def peek2():
    ins = whatTheFrame.FrameInspectorBase()
    frame_info = list()
    for f in whatTheFrame.ReverseFromCurrentFrame(start_distance=3):
        frame_info.append(ins.inspect(f))
    pp(frame_info)


class Test_(unittest.TestCase):

    def setUp(self):
        suicideCore.this_is_critical_orig = suicideCore.this_is_critical
        suicideCore.this_is_critical = func

    def tearDown(self):
        suicideCore.this_is_critical = suicideCore.this_is_critical_orig

    def test_(self):
        gloryApp.run()


if __name__ == '__main__':
    unittest.main()
