import unittest

from kappaschedules.schedules.periodic_bool_schedule import PeriodicBoolSchedule
from kappaschedules.factory import object_to_schedule

class TestPeriodicBoolSchedule(unittest.TestCase):
    def _test(self, expected, initial_state, on_duration, off_duration, on_value=None, off_value=None, invert=False):
        kwargs = {}
        if on_value is not None:
            kwargs["on_value"] = on_value
        if off_value is not None:
            kwargs["off_value"] = off_value
        sched = PeriodicBoolSchedule(
            initial_state=initial_state,
            on_duration=on_duration,
            off_duration=off_duration,
            invert=invert,
            **kwargs,
        )
        actual = [sched.get_value(step=i, total_steps=len(expected)) for i in range(len(expected))]
        self.assertEqual(expected, actual)

    def test_off1_on1(self):
        self._test(
            expected=[0, 1, 0, 1, 0, 1],
            initial_state=False,
            on_duration=1,
            off_duration=1,
        )

    def test_on1_off1(self):
        self._test(
            expected=[1, 0, 1, 0, 1, 0],
            initial_state=True,
            on_duration=1,
            off_duration=1,
        )

    def test_on1_off1_onvalue075(self):
        self._test(
            expected=[0.75, 0, 0.75, 0, 0.75, 0],
            initial_state=True,
            on_duration=1,
            off_duration=1,
            on_value=0.75,
        )

    def test_on1_off1_offvalue025(self):
        self._test(
            expected=[1, 0.25, 1, 0.25, 1, 0.25],
            initial_state=True,
            on_duration=1,
            off_duration=1,
            off_value=0.25,
        )

    def test_on1_off0(self):
        self._test(
            expected=[1, 1, 1, 1, 1, 1, 1],
            initial_state=True,
            on_duration=1,
            off_duration=0,
        )

    def test_on3_off1(self):
        self._test(
            expected=[1, 1, 1, 0, 1, 1, 1],
            initial_state=True,
            on_duration=3,
            off_duration=1,
        )

    def test_on3_off4(self):
        self._test(
            expected=[1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            initial_state=True,
            on_duration=3,
            off_duration=4,
        )

    def test_off4_on3(self):
        self._test(
            expected=[0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            initial_state=False,
            on_duration=3,
            off_duration=4,
        )

    def test_invert(self):
        self._test(
            expected=[1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            initial_state=False,
            on_duration=3,
            off_duration=4,
            invert=True,
        )

    def test_factory_set_onvalue_with_maxvalue(self):
        schedule = object_to_schedule(
            dict(
                kind="periodic_bool_schedule",
                initial_state=False,
                on_duration=2,
                off_duration=1,
                invert=True,
            ),
            max_value=0.75,
        )
        self.assertIsInstance(schedule, PeriodicBoolSchedule)
        self.assertEqual(0.75, schedule.on_value)
