import unittest

from kappaschedules import LinearIncreasingSchedule, CosineDecreasingSchedule, SequentialStepSchedule, SequentialStepScheduleConfig
from tests_utils.asserts import assertIsClose


class TestWarmupCosine(unittest.TestCase):
    def test_zero_to_one(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(end_step=4, schedule=LinearIncreasingSchedule(exclude_first=True, exclude_last=True)),
            SequentialStepScheduleConfig(schedule=CosineDecreasingSchedule(exclude_last=True)),
        ])
        total_steps = 10
        values = [sched.get_value(i, total_steps) for i in range(total_steps)]
        assertIsClose(self, [0.2, 0.4, 0.6, 0.8, 1.0, 0.933, 0.75, 0.5, 0.25, 0.067], values)
