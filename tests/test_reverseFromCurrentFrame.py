
import unittest

import mock

from whatTheFrame import ReverseFromCurrentFrame


class FakeFrame(object):

    def __init__(self, f_back=None):
        self.f_back = f_back

    @classmethod
    def create(cls, num=5):
        f = cls()
        if num > 1:
            for _ in xrange(num - 1):
                f = cls(f_back=f)
        return f


class TestReverseFromCurrentFrame(unittest.TestCase):

    def setUp(self):
        self.currentframe = mock.MagicMock()
        self.patcher = mock.patch('inspect.currentframe', self.currentframe)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_expectEmptyFrame(self):
        self.currentframe.return_value = FakeFrame()
        self.assertFalse(list(ReverseFromCurrentFrame()))

    def test_expectNumFrames(self):
        self.currentframe.return_value = FakeFrame.create(num=2)
        self.assertEqual(2, len(list(ReverseFromCurrentFrame(start_distance=0, max_distance=-1))))
        self.currentframe.return_value = FakeFrame.create(num=12)
        self.assertEqual(12, len(list(ReverseFromCurrentFrame(start_distance=0, max_distance=-1))))

    def test_withStartDistance_expectNumFrames(self):
        self.currentframe.return_value = FakeFrame.create(num=12)
        self.assertEqual(8, len(list(ReverseFromCurrentFrame(start_distance=4, max_distance=-1))))
        self.currentframe.return_value = FakeFrame.create(num=2)
        self.assertEqual(0, len(list(ReverseFromCurrentFrame(start_distance=3, max_distance=-1))))

    def test_withMaxDistance_expectNumFrames(self):
        self.currentframe.return_value = FakeFrame.create(num=12)
        self.assertEqual(5, len(list(ReverseFromCurrentFrame(start_distance=0, max_distance=4))))

