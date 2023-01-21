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

