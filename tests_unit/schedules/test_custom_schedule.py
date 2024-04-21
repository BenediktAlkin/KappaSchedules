import unittest

import numpy as np
import torch

from kappaschedules.schedules import CustomSchedule


class TestCustomSchedule(unittest.TestCase):
    def test(self):
        values = torch.rand(size=(11,), generator=torch.Generator().manual_seed(94)).tolist()
        sched = CustomSchedule(values=values)
        actual = [sched.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(values, actual), actual)
