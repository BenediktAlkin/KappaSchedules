import unittest

from kappaschedules.sequential_schedule import SequentialSchedule, SequentialScheduleConfig

from tests_utils.dummy_schedule import DummySchedule

class TestSequentialSchedule(unittest.TestCase):
    def test_propagate_singleconfig(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertIsNone(sched.schedule_configs[0].end_step)

    def test_propagate_forward(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_backward(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(schedule=DummySchedule()),
            SequentialScheduleConfig(start_step=10, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_gap(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialScheduleConfig(start_step=15, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(15, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_noneinbetween(self):
        with self.assertRaises(AssertionError):
            SequentialSchedule([
                SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
                SequentialScheduleConfig(schedule=DummySchedule()),
                SequentialScheduleConfig(start_step=15, schedule=DummySchedule()),
            ])

    def test_check_singleconfig(self):
        with self.assertRaises(AssertionError):
            SequentialSchedule([
                SequentialScheduleConfig(start_step=5, end_step=3, schedule=DummySchedule()),
            ])

    def test_check_propagatedendstep(self):
        with self.assertRaises(AssertionError):
            SequentialSchedule([
                SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
                SequentialScheduleConfig(start_step=5, schedule=DummySchedule()),
            ])
