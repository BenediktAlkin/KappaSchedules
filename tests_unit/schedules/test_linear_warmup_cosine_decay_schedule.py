import unittest

import numpy as np

from kappaschedules.factory import object_to_schedule


class TestLinearWarmupCosineDecaySchedule(unittest.TestCase):
    def test_factory_percent(self):
        schedule = object_to_schedule(
            dict(
                kind="linear_warmup_cosine_decay_schedule",
                warmup_percent=0.2,
            )
        )
        expected = [
            0.3333333333333333,
            0.6666666666666666,
            1.0,
            0.9619398043158771,
            0.8535535370398831,
            0.6913420248408287,
            0.5000005000000001,
            0.3086589751591714,
            0.1464474629601169,
            0.03806119568412292,
            1e-06
        ]
        actual = [schedule.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_factory_epoch(self):
        schedule = object_to_schedule(
            dict(
                kind="linear_warmup_cosine_decay_schedule",
                warmup_epochs=1,
            ),
            updates_per_epoch=2,
        )
        expected = [
            0.3333333333333333,
            0.6666666666666666,
            1.0,
            0.9619398043158771,
            0.8535535370398831,
            0.6913420248408287,
            0.5000005000000001,
            0.3086589751591714,
            0.1464474629601169,
            0.03806119568412292,
            1e-06
        ]
        actual = [schedule.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_factory_update(self):
        schedule = object_to_schedule(
            dict(
                kind="linear_warmup_cosine_decay_schedule",
                warmup_updates=2,
            ),
        )
        expected = [
            0.3333333333333333,
            0.6666666666666666,
            1.0,
            0.9619398043158771,
            0.8535535370398831,
            0.6913420248408287,
            0.5000005000000001,
            0.3086589751591714,
            0.1464474629601169,
            0.03806119568412292,
            1e-06
        ]
        actual = [schedule.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)

    def test_factory_samples(self):
        schedule = object_to_schedule(
            dict(
                kind="linear_warmup_cosine_decay_schedule",
                warmup_samples=15,
            ),
            batch_size=8
        )
        expected = [
            0.3333333333333333,
            0.6666666666666666,
            1.0,
            0.9619398043158771,
            0.8535535370398831,
            0.6913420248408287,
            0.5000005000000001,
            0.3086589751591714,
            0.1464474629601169,
            0.03806119568412292,
            1e-06
        ]
        actual = [schedule.get_value(step, total_steps=11) for step in range(11)]
        self.assertTrue(np.allclose(expected, actual), actual)
