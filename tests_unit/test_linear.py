import unittest

import numpy as np

from kappaschedules.linear_decreasing import LinearDecreasing
from kappaschedules.linear_increasing import LinearIncreasing


class TestLinear(unittest.TestCase):
    def test_invalid_abs(self):
        with self.assertRaises(AssertionError):
            LinearIncreasing(abs_start_value=2., exclude_last=False)
        with self.assertRaises(AssertionError):
            LinearDecreasing(abs_end_value=2., exclude_last=False)

    def test_increasing(self):
        sched = LinearIncreasing(exclude_last=False)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.], actual))

    def test_increasing_excludelast(self):
        sched = LinearIncreasing(exclude_last=True)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        expected = [
            0.0,
            0.0909090909090909,
            0.1818181818181818,
            0.2727272727272727,
            0.3636363636363636,
            0.4545454545454545,
            0.5454545454545454,
            0.6363636363636364,
            0.7272727272727272,
            0.8181818181818181,
            0.9090909090909090,
        ]
        self.assertTrue(np.allclose(expected, actual))

    def test_increasing_excludefirst(self):
        sched = LinearIncreasing(exclude_first=True)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        expected = [
            0.0909090909090909,
            0.1818181818181818,
            0.2727272727272727,
            0.3636363636363636,
            0.4545454545454545,
            0.5454545454545454,
            0.6363636363636363,
            0.7272727272727272,
            0.8181818181818181,
            0.9090909090909090,
            1.0
        ]
        self.assertTrue(np.allclose(expected, actual))

    def test_increasing_excludeboth(self):
        sched = LinearIncreasing(exclude_first=True, exclude_last=True)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        expected = [
            0.08333333333333333,
            0.16666666666666666,
            0.25,
            0.3333333333333333,
            0.4166666666666666,
            0.5,
            0.5833333333333333,
            0.6666666666666666,
            0.75,
            0.8333333333333333,
            0.9166666666666666,
        ]
        self.assertTrue(np.allclose(expected, actual))

    def test_increasing_absmin(self):
        sched = LinearIncreasing(exclude_last=False, abs_start_value=1e-5)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        expected = [
            1e-05,
            0.100009,
            0.200008,
            0.300007,
            0.400006,
            0.500005,
            0.600004,
            0.700003,
            0.800002,
            0.900001,
            1.0,
        ]
        self.assertTrue(np.allclose(expected, actual))

    def test_decreasing(self):
        sched = LinearDecreasing(exclude_last=False)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0], actual))

    def test_decreasing_exclude(self):
        sched = LinearDecreasing(exclude_last=True)
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
