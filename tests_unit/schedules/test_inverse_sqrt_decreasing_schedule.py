import unittest

import numpy as np

from kappaschedules.schedules.inverse_sqrt_decreasing_schedule import InverseSqrtDecreasingSchedule


class TestInverseSqrtDecreasingSchedule(unittest.TestCase):
    def test_decreasing(self):
        sched = InverseSqrtDecreasingSchedule(warmup_steps=10)
        expected = [
            1.0,
            0.9534625892455924,
            0.9128709291752769,
            0.8770580193070293,
            0.8451542547285167,
            0.8164965809277261,
            0.7905694150420949,
            0.7669649888473705,
            0.7453559924999299,
            0.7254762501100117,
            0.7071067811865476,
        ]
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

