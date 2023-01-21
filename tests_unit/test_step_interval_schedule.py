import unittest

import numpy as np

from kappaschedules.schedules.step_interval_schedule import StepIntervalSchedule


class TestStepIntervalSchedule(unittest.TestCase):
    def test_invalid_interval(self):
        with self.assertRaises(AssertionError):
            StepIntervalSchedule(start_value=1., factor=0.5, interval=0.)
        with self.assertRaises(AssertionError):
            StepIntervalSchedule(start_value=1., factor=0.5, interval=1.)

    def test_increasing(self):
        sched = StepIntervalSchedule(start_value=1., factor=1.5, interval=0.2)
        actual = [sched.get_value(step, total_steps=10) for step in range(10)]
        self.assertTrue(np.allclose([1., 1., 1.5, 1.5, 2.25, 2.25, 3.375, 3.375, 5.0625, 5.0625], actual))

    def test_decreasing(self):
        sched = StepIntervalSchedule(start_value=1., factor=0.5, interval=0.2)
        actual = [sched.get_value(step, total_steps=10) for step in range(10)]
        self.assertTrue(np.allclose([1., 1., 0.5, 0.5, 0.25, 0.25, 0.125, 0.125, 0.0625, 0.0625], actual))
