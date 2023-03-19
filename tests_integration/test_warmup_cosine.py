import unittest

import kappaschedules as ks
from tests_utils.asserts import assertIsClose


class TestWarmupCosine(unittest.TestCase):
    def test_step_zero_to_one(self):
        sched = ks.SequentialStepSchedule([
            ks.SequentialStepScheduleConfig(
                end_step=4,
                schedule=ks.LinearIncreasingSchedule(exclude_first=True, exclude_last=True),
            ),
            ks.SequentialStepScheduleConfig(schedule=ks.CosineDecreasingSchedule(exclude_last=True)),
        ])
        total_steps = 10
        values = [sched.get_value(i, total_steps) for i in range(total_steps)]
        assertIsClose(self, [0.2, 0.4, 0.6, 0.8, 1.0, 0.933, 0.75, 0.5, 0.25, 0.067], values)

    def test_percent_zero_to_one(self):
        sched = ks.SequentialPercentSchedule([
            ks.SequentialPercentScheduleConfig(
                # percentages are from 0 to 100 -> end_percent 0.4 would not correspond to end_step=4
                # end_step = end_percent * (total_steps - 1)
                # 4.05 = 0.45 * (10 - 1)
                end_percent=0.45,
                schedule=ks.LinearIncreasingSchedule(exclude_first=True, exclude_last=True),
            ),
            ks.SequentialPercentScheduleConfig(schedule=ks.CosineDecreasingSchedule(exclude_last=True)),
        ])
        total_steps = 10
        values = [sched.get_value(i, total_steps) for i in range(total_steps)]
        assertIsClose(self, [0.2, 0.4, 0.6, 0.8, 1.0, 0.933, 0.75, 0.5, 0.25, 0.067], values)

    def test_percent_equal_to_step(self):
        percent = ks.SequentialPercentSchedule([
            ks.SequentialPercentScheduleConfig(
                end_percent=0.1,
                schedule=ks.LinearIncreasingSchedule(exclude_first=True, exclude_last=True),
            ),
            ks.SequentialPercentScheduleConfig(
                schedule=ks.CosineDecreasingSchedule(exclude_last=True),
            ),
        ])
        step = ks.SequentialStepSchedule([
            ks.SequentialStepScheduleConfig(
                end_step=19,
                schedule=ks.LinearIncreasingSchedule(exclude_first=True, exclude_last=True),
            ),
            ks.SequentialStepScheduleConfig(
                schedule=ks.CosineDecreasingSchedule(exclude_last=True),
            ),
        ])
        total_steps = 194
        percent_values = [percent.get_value(i, total_steps) for i in range(total_steps)]
        step_values = [step.get_value(i, total_steps) for i in range(total_steps)]
        self.assertEqual(percent_values, step_values)
