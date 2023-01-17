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

    def test_propagate_middle(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialScheduleConfig(schedule=DummySchedule()),
            SequentialScheduleConfig(start_step=15, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertEqual(15, sched.schedule_configs[1].end_step)
        self.assertEqual(15, sched.schedule_configs[2].start_step)
        self.assertIsNone(sched.schedule_configs[2].end_step)

    def test_propagate_noneinbetween(self):
        with self.assertRaises(AssertionError):
            SequentialSchedule([
                SequentialScheduleConfig(end_step=10, schedule=DummySchedule()),
                SequentialScheduleConfig(schedule=DummySchedule()),
                SequentialScheduleConfig(schedule=DummySchedule()),
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

    def test_get_sequential_schedule_config_zeroduration(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(end_step=0, schedule=DummySchedule()),
            SequentialScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(0))

    def test_get_sequential_schedule_config(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(start_step=5, end_step=10, schedule=DummySchedule()),
            SequentialScheduleConfig(end_step=15, schedule=DummySchedule()),
            SequentialScheduleConfig(schedule=DummySchedule()),
        ])
        for i in range(5):
            self.assertIsNone(sched.get_sequential_schedule_config(i))
        for i in range(5, 10):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i))
        for i in range(10, 15):
            self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(i))
        for i in range(15, 30):
            self.assertEqual(sched.schedule_configs[2], sched.get_sequential_schedule_config(i))

    def test_get_sequential_schedule_config_gap(self):
        sched = SequentialSchedule([
            SequentialScheduleConfig(start_step=5, end_step=10, schedule=DummySchedule()),
            SequentialScheduleConfig(start_step=15, end_step=20, schedule=DummySchedule()),
            SequentialScheduleConfig(schedule=DummySchedule()),
        ])
        for i in range(5):
            self.assertIsNone(sched.get_sequential_schedule_config(i))
        for i in range(5, 10):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i))
        # gap returns previous schedule
        for i in range(10, 15):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i))
        for i in range(15, 20):
            self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(i))
        for i in range(20, 30):
            self.assertEqual(sched.schedule_configs[2], sched.get_sequential_schedule_config(i))
