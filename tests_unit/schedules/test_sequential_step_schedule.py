import unittest

from kappaschedules.schedules.sequential_step_schedule import SequentialStepSchedule, SequentialStepScheduleConfig
from tests_utils.dummy_schedule import DummySchedule


class TestSequentialStepSchedule(unittest.TestCase):
    def test_propagate_singleconfig(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertIsNone(sched.schedule_configs[0].end_step)

    def test_propagate_forward(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialStepScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_backward(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(schedule=DummySchedule()),
            SequentialStepScheduleConfig(start_step=10, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_gap(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialStepScheduleConfig(start_step=15, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(15, sched.schedule_configs[1].start_step)
        self.assertIsNone(sched.schedule_configs[1].end_step)

    def test_propagate_middle(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(end_step=10, schedule=DummySchedule()),
            SequentialStepScheduleConfig(schedule=DummySchedule()),
            SequentialStepScheduleConfig(start_step=15, schedule=DummySchedule()),
        ])
        self.assertEqual(0, sched.schedule_configs[0].start_step)
        self.assertEqual(10, sched.schedule_configs[0].end_step)
        self.assertEqual(10, sched.schedule_configs[1].start_step)
        self.assertEqual(15, sched.schedule_configs[1].end_step)
        self.assertEqual(15, sched.schedule_configs[2].start_step)
        self.assertIsNone(sched.schedule_configs[2].end_step)

    def test_propagate_noneinbetween(self):
        with self.assertRaises(AssertionError):
            SequentialStepSchedule([
                SequentialStepScheduleConfig(end_step=10, schedule=DummySchedule()),
                SequentialStepScheduleConfig(schedule=DummySchedule()),
                SequentialStepScheduleConfig(schedule=DummySchedule()),
            ])

    def test_check_singleconfig(self):
        with self.assertRaises(AssertionError):
            SequentialStepSchedule([
                SequentialStepScheduleConfig(start_step=5, end_step=3, schedule=DummySchedule()),
            ])

    def test_check_propagatedendstep(self):
        with self.assertRaises(AssertionError):
            SequentialStepSchedule([
                SequentialStepScheduleConfig(end_step=10, schedule=DummySchedule()),
                SequentialStepScheduleConfig(start_step=5, schedule=DummySchedule()),
            ])

    def test_get_sequential_schedule_config_zeroduration(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(end_step=0, schedule=DummySchedule()),
            SequentialStepScheduleConfig(schedule=DummySchedule()),
        ])
        self.assertEqual(sched.schedule_configs[1], sched.get_sequential_schedule_config(0))

    def test_get_sequential_schedule_config(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(start_step=5, end_step=10, schedule=DummySchedule()),
            SequentialStepScheduleConfig(end_step=15, schedule=DummySchedule()),
            SequentialStepScheduleConfig(schedule=DummySchedule()),
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
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(start_step=5, end_step=10, schedule=DummySchedule()),
            SequentialStepScheduleConfig(start_step=15, end_step=20, schedule=DummySchedule()),
            SequentialStepScheduleConfig(schedule=DummySchedule()),
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

    def test_get_value_before_first_schedule(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(start_step=5, schedule=DummySchedule(step_to_value={0: 0.5})),
        ])
        for i in range(5):
            self.assertEqual(0.5, sched.get_value(i, 10))

    def test_get_value_after_last_schedule(self):
        sched = SequentialStepSchedule([
            SequentialStepScheduleConfig(start_step=3, end_step=5, schedule=DummySchedule(step_to_value={0: 0.1, 1: 0.2})),
        ])
        for i in range(4):
            self.assertEqual(0.1, sched.get_value(i, 10))
        self.assertEqual(0.2, sched.get_value(4, 10))
        for i in range(5, 10):
            self.assertEqual(0.2, sched.get_value(i, 10))
