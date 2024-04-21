import unittest

import numpy as np

from kappaschedules.schedules.cosine_decreasing_schedule import CosineDecreasingSchedule


class TestCosineDecreasingSchedule(unittest.TestCase):
    def test_decreasing(self):
        sched = CosineDecreasingSchedule()
        expected = [
            1.0,
            0.9755282581475768,
            0.9045084971874737,
            0.7938926261462366,
            0.6545084971874737,
            0.5,
            0.3454915028125263,
            0.20610737385376354,
            0.09549150281252627,
            0.02447174185242318,
            0.0,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_decreasing_overhang(self):
        sched = CosineDecreasingSchedule()
        sched_percent = CosineDecreasingSchedule(overhang_percent=0.25)
        sched_steps = CosineDecreasingSchedule(overhang_steps=2)
        expected = [
            1.0,
            0.9829629131445341,
            0.9330127018922194,
            0.8535533905932737,
            0.75,
            0.6294095225512604,
            0.5,
            0.37059047744873963,
            0.2500000000000001,
            0.14644660940672627,
            0.06698729810778059
        ]
        actual = [sched.get_value(step, total_steps=11 + int(11 * 0.25)) for step in range(11)]
        actual_percent = [sched_percent.get_value(step, total_steps=11) for step in range(11)]
        actual_steps = [sched_steps.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)
        self.assertTrue(np.allclose(expected, actual_percent), actual_percent)
        self.assertTrue(np.allclose(expected, actual_steps), actual_steps)
