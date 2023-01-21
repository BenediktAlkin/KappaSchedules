import unittest

import kappaschedules as ks

class TestFactory(unittest.TestCase):
    def test_none(self):
        self.assertIsNone(ks.object_to_schedule(None))

    def test_already_created(self):
        self.assertIsInstance(ks.object_to_schedule(ks.LinearIncreasingSchedule()), ks.LinearIncreasingSchedule)

    def test_single(self):
        sched = ks.object_to_schedule(dict(kind="linear_increasing_schedule"))
        self.assertIsInstance(sched, ks.LinearIncreasingSchedule)

    def test_sequential_unspecified(self):
        sched = ks.object_to_schedule([dict(schedule=dict(kind="linear_increasing_schedule"))])
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_sequential_percent(self):
        sched = ks.object_to_schedule([
            dict(
                schedule=dict(kind="linear_increasing_schedule"),
                end_percent=0.5,
            ),
        ])
        self.assertIsInstance(sched, ks.SequentialPercentSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_sequential_step(self):
        sched = ks.object_to_schedule([
            dict(
                schedule=dict(kind="linear_increasing_schedule"),
                end_step=2,
            ),
        ])
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_explicit_sequential_percent(self):
        sched = ks.object_to_schedule(dict(
            kind="sequential_percent_schedule",
            schedule_configs=[
                dict(schedule=dict(kind="linear_increasing_schedule"), end_percent=0.8),
            ],
        ))
        self.assertIsInstance(sched, ks.SequentialPercentSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_explicit_sequential_step(self):
        sched = ks.object_to_schedule(dict(
            kind="sequential_step_schedule",
            schedule_configs=[
                dict(schedule=dict(kind="linear_increasing_schedule"), end_step=2),
            ],
        ))
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)
