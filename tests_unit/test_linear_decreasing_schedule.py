import unittest

import numpy as np

from kappaschedules.schedules.linear_decreasing_schedule import LinearDecreasingSchedule


class TestLinear(unittest.TestCase):
    def test_invalid_abs(self):
        with self.assertRaises(AssertionError):
            LinearDecreasingSchedule(end_value=2., exclude_last=False)

    def test_decreasing(self):
        sched = LinearDecreasingSchedule(exclude_last=False)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0], actual))

    def test_decreasing_exclude(self):
        sched = LinearDecreasingSchedule(exclude_last=True)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        expected = [
            1.0,
            0.9090909090909090,
            0.8181818181818181,
            0.7272727272727272,
            0.6363636363636363,
            0.5454545454545454,
            0.4545454545454545,
            0.3636363636363636,
            0.2727272727272727,
            0.1818181818181818,
            0.0909090909090909,
        ]
        self.assertTrue(np.allclose(expected, actual))
