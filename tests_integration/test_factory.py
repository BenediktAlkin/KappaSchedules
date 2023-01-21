import unittest

from kappaschedules import object_to_schedule, LinearIncreasingSchedule, SequentialSchedule

class TestFactory(unittest.TestCase):
    def test_single(self):
        sched = object_to_schedule(dict(kind="linear_increasing_schedule"))
        self.assertIsInstance(sched, LinearIncreasingSchedule)

    def test_sequential(self):
        sched = object_to_schedule([dict(schedule=dict(kind="linear_increasing_schedule"))])
        self.assertIsInstance(sched, SequentialSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, LinearIncreasingSchedule)
