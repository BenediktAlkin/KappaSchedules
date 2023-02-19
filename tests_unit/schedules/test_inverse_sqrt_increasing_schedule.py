import unittest

import numpy as np

from kappaschedules.schedules.inverse_sqrt_increasing_schedule import InverseSqrtIncreasingSchedule


class TestInverseSqrtIncreasingSchedule(unittest.TestCase):
    def test_increasing(self):
        sched = InverseSqrtIncreasingSchedule()
        expected = [
            0.0,
            0.2928932188134524,
            0.42264973081037427,
            0.5,
            0.5527864045000421,
            0.591751709536137,
            0.6220355269907727,
            0.6464466094067263,
            0.6666666666666667,
            0.683772233983162,
            0.6984886554222364,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)


    def test_increasing_warmup(self):
        sched = InverseSqrtIncreasingSchedule()
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
        actual = [sched.get_value(step, total_steps=11, abs_step=step + 10) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

