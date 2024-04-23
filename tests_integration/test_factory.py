import unittest

import kappaschedules as ks


class TestFactory(unittest.TestCase):
    def test_none(self):
        self.assertIsNone(ks.object_to_schedule(None))

    def test_already_created(self):
        self.assertIsInstance(ks.object_to_schedule(ks.LinearIncreasingSchedule()), ks.LinearIncreasingSchedule)

    def test_single(self):
        sched = ks.object_to_schedule(dict(kind="linear_increasing_schedule"), max_value=0.8)
        self.assertIsInstance(sched, ks.LinearIncreasingSchedule)
        self.assertEqual(0.0, sched.start_value)
        self.assertEqual(0.8, sched.delta)

    def test_sequential_unspecified(self):
        sched = ks.object_to_schedule([dict(schedule=dict(kind="linear_increasing_schedule"))])
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_sequential_mixed(self):
        with self.assertRaises(AssertionError):
            ks.object_to_schedule([
                dict(schedule=dict(kind="linear_increasing_schedule"), end_percent=0.3),
                dict(schedule=dict(kind="linear_increasing_schedule"), end_step=5),
            ])

    def test_sequential_no_schedule(self):
        with self.assertRaises(AssertionError):
            ks.object_to_schedule([dict(end_percent=0.3)])

    def test_sequential_percent(self):
        sched = ks.object_to_schedule([
            dict(
                schedule=dict(kind="linear_increasing_schedule"),
                end_percent=0.5,
            ),
        ])
        self.assertIsInstance(sched, ks.SequentialPercentSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_sequential_percent_propagate_max_value(self):
        sched = ks.object_to_schedule([
            dict(schedule=dict(kind="linear_increasing_schedule"), end_percent=0.3),
            dict(schedule=dict(kind="cosine_decreasing_schedule")),
        ], max_value=0.8)
        self.assertIsInstance(sched, ks.SequentialPercentSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)
        self.assertIsInstance(sched.schedule_configs[1].schedule, ks.CosineDecreasingSchedule)
        self.assertEqual(0.0, sched.schedule_configs[0].schedule.start_value)
        self.assertEqual(0.8, sched.schedule_configs[0].schedule.delta)
        self.assertEqual(0.8, sched.schedule_configs[1].schedule.start_value)
        self.assertEqual(-0.8, sched.schedule_configs[1].schedule.delta)

    def test_sequential_step(self):
        sched = ks.object_to_schedule([
            dict(
                schedule=dict(kind="linear_increasing_schedule"),
                end_step=2,
            ),
        ])
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.LinearIncreasingSchedule)

    def test_sequential_constant_maxvalue(self):
        sched = ks.object_to_schedule(
            [
                dict(
                    schedule=dict(kind="constant_schedule", value=0.1),
                    end_step=2,
                ),
            ],
            max_value=0.1,
        )
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.ConstantSchedule)

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

    def test_periodic_bool_schedule(self):
        sched = ks.object_to_schedule(
            dict(
                kind="periodic_bool_schedule",
                initial_state=True,
            ),
        )
        self.assertIsInstance(sched, ks.PeriodicBoolSchedule)

    def test_sequential_include_maxvalue_when_ctor_is_overridden(self):
        sched = ks.object_to_schedule(
            [
                dict(
                    schedule=dict(
                        kind="polynomial_decreasing_schedule",
                        power=1.0,
                    ),
                ),
            ],
            max_value=0.1,
        )
        self.assertIsInstance(sched, ks.SequentialStepSchedule)
        self.assertIsInstance(sched.schedule_configs[0].schedule, ks.PolynomialDecreasingSchedule)
        self.assertEqual(-0.1, sched.schedule_configs[0].schedule.delta)

    def test_constant(self):
        sched = ks.object_to_schedule(0.3)
        self.assertIsInstance(sched, ks.ConstantSchedule)
        self.assertEqual(0.3, sched.value)

    def test_custom(self):
        sched = ks.object_to_schedule([0.3, 0.4])
        self.assertIsInstance(sched, ks.CustomSchedule)
        values = [sched.get_value(step=i, total_steps=2) for i in range(2)]
        self.assertEqual([0.3, 0.4], values)
