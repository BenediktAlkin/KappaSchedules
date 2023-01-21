from kappaschedules.schedules.base import ScheduleBase


class DummySchedule(ScheduleBase):
    def __init__(self, step_to_value=None):
        super().__init__()
        self.step_to_value = step_to_value

    def _get_value(self, step: int, total_steps: int) -> float:
        if self.step_to_value is None:
            return 0.
        return self.step_to_value[step]

    def __str__(self):
        return "Dummy"
