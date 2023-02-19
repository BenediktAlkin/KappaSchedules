import unittest

import numpy as np

from kappaschedules.schedules.inverse_sqrt_increasing_schedule import InverseSqrtIncreasingSchedule


class TestInverseSqrtIncreasingSchedule(unittest.TestCase):
    def test_increasing(self):
        sched = InverseSqrtIncreasingSchedule(warmup_steps=10)
        expected = [
            0.0,
            0.04653741075440765,
            0.0871290708247231,
            0.12294198069297069,
            0.15484574527148331,
            0.18350341907227385,
            0.20943058495790512,
            0.23303501115262948,
            0.2546440075000701,
            0.2745237498899883,
            0.2928932188134524,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

