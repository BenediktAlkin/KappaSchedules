import unittest

from kappaschedules import SequentialPercentSchedule, SequentialPercentScheduleConfig
from tests_utils.dummy_schedule import DummySchedule


class TestSequentialPercentSchedule(unittest.TestCase):
    def test_propagate_singleconfig(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0.0, sched.schedule_configs[0].start_percent)
        self.assertEqual(1.0, sched.schedule_configs[0].end_percent)

    def test_propagate_forward(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(end_percent=0.1, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0.0, sched.schedule_configs[0].start_percent)
        self.assertEqual(0.1, sched.schedule_configs[0].end_percent)
        self.assertEqual(0.1, sched.schedule_configs[1].start_percent)
        self.assertEqual(1.0, sched.schedule_configs[1].end_percent)

    def test_propagate_backward(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
            SequentialPercentScheduleConfig(start_percent=0.1, schedule=DummySchedule()),
        ])
        self.assertEqual(0.0, sched.schedule_configs[0].start_percent)
        self.assertEqual(0.1, sched.schedule_configs[0].end_percent)
        self.assertEqual(0.1, sched.schedule_configs[1].start_percent)
        self.assertEqual(1.0, sched.schedule_configs[1].end_percent)

    def test_propagate_gap(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(end_percent=0.1, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(start_percent=0.15, schedule=DummySchedule()),
        ])
        self.assertEqual(0.0, sched.schedule_configs[0].start_percent)
        self.assertEqual(0.1, sched.schedule_configs[0].end_percent)
        self.assertEqual(0.15, sched.schedule_configs[1].start_percent)
        self.assertEqual(1.0, sched.schedule_configs[1].end_percent)

    def test_propagate_middle(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(end_percent=0.1, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
            SequentialPercentScheduleConfig(start_percent=0.15, schedule=DummySchedule()),
        ])
        self.assertEqual(0.0, sched.schedule_configs[0].start_percent)
        self.assertEqual(0.1, sched.schedule_configs[0].end_percent)
        self.assertEqual(0.1, sched.schedule_configs[1].start_percent)
        self.assertEqual(0.15, sched.schedule_configs[1].end_percent)
        self.assertEqual(0.15, sched.schedule_configs[2].start_percent)
        self.assertEqual(1.0, sched.schedule_configs[2].end_percent)

    def test_propagate_noneinbetween(self):
        with self.assertRaises(AssertionError):
            SequentialPercentSchedule([
                SequentialPercentScheduleConfig(end_percent=0.1, schedule=DummySchedule()),
                SequentialPercentScheduleConfig(schedule=DummySchedule()),
                SequentialPercentScheduleConfig(schedule=DummySchedule()),
            ])

    def test_check_singleconfig(self):
        with self.assertRaises(AssertionError):
            SequentialPercentSchedule([
                SequentialPercentScheduleConfig(start_percent=0.5, end_percent=0.3, schedule=DummySchedule()),
            ])

    def test_check_propagatedendstep(self):
        with self.assertRaises(AssertionError):
            SequentialPercentSchedule([
                SequentialPercentScheduleConfig(end_percent=0.1, schedule=DummySchedule()),
                SequentialPercentScheduleConfig(start_percent=0.05, schedule=DummySchedule()),
            ])

    def test_get_sequential_schedule_config_zeroduration(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(end_percent=0.0, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(0, 10))

    def test_get_sequential_schedule_config(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(start_percent=0.05, end_percent=0.1, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(end_percent=0.15, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
        ])
        for i in range(5):
            self.assertIsNone(sched.get_sequential_schedule_config(i, 101))
        for i in range(5, 10):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i, 101))
        for i in range(10, 15):
            self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(i, 101))
        for i in range(15, 30):
            self.assertEqual(sched.schedule_configs[2], sched.get_sequential_schedule_config(i, 101))

    def test_get_sequential_schedule_config_gap(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(start_percent=0.05, end_percent=0.1, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(start_percent=0.15, end_percent=0.2, schedule=DummySchedule()),
            SequentialPercentScheduleConfig(schedule=DummySchedule()),
        ])
        for i in range(5):
            self.assertIsNone(sched.get_sequential_schedule_config(i, 101))
        for i in range(5, 10):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i, 101))
        # gap returns previous schedule
        for i in range(10, 15):
            self.assertEqual(sched.schedule_configs[0], sched.get_sequential_schedule_config(i, 101))
        for i in range(15, 20):
            self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(i, 101))
        for i in range(20, 30):
            self.assertEqual(sched.schedule_configs[2], sched.get_sequential_schedule_config(i, 101))

    def test_get_value_before_first_schedule(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(start_percent=0.5, schedule=DummySchedule(step_to_value={0: 0.5})),
        ])
        for i in range(5):
            self.assertEqual(0.5, sched.get_value(i, 10))

    def test_get_value_after_last_schedule(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(
                start_percent=0.3,
                end_percent=0.5,
                schedule=DummySchedule(step_to_value={0: 0.1, 1: 0.2}),
            ),
        ])
        for i in range(4):
            self.assertEqual(0.1, sched.get_value(i, 10))
        self.assertEqual(0.2, sched.get_value(4, 10))
        for i in range(5, 10):
            self.assertEqual(0.2, sched.get_value(i, 10))

    def test_tostring(self):
        sched = SequentialPercentSchedule([
            SequentialPercentScheduleConfig(
                start_percent=0.3,
                end_percent=0.5,
                schedule=DummySchedule(),
            ),
        ])
        lines = str(sched).split("\n")
        self.assertEqual(3, len(lines))
        self.assertEqual(SequentialPercentSchedule.__name__, lines[0])
        self.assertEqual("  (0): 30% - 50% Dummy", lines[1])
        self.assertEqual(")", lines[2])