import unittest

import numpy as np

from kappaschedules.schedules.step_fixed_schedule import StepFixedSchedule


class TestStepFixedSchedule(unittest.TestCase):
    def test_invalid_steps(self):
        with self.assertRaises(AssertionError):
            StepFixedSchedule(start_value=1., factor=0.5, steps=None)
        with self.assertRaises(AssertionError):
            StepFixedSchedule(start_value=1., factor=0.5, steps=[])
        with self.assertRaises(AssertionError):
            StepFixedSchedule(start_value=1., factor=0.5, steps=[5])
        with self.assertRaises(AssertionError):
            StepFixedSchedule(start_value=1., factor=0.5, steps=[-1])

    def test_increasing(self):
        sched = StepFixedSchedule(start_value=1., factor=1.5, steps=[0.2, 0.5, 0.8])
        actual = [sched.get_value(step, total_steps=10) for step in range(10)]
        self.assertTrue(np.allclose([1., 1., 1.5, 1.5, 1.5, 2.25, 2.25, 2.25, 3.375, 3.375], actual))

    def test_decreasing(self):
        sched = StepFixedSchedule(start_value=1., factor=0.5, steps=[0.2, 0.5, 0.8])
        actual = [sched.get_value(step, total_steps=10) for step in range(10)]
        self.assertTrue(np.allclose([1., 1., 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0.125, 0.125], actual))
