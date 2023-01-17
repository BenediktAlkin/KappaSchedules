from .base.schedule_base import ScheduleBase


class Constant(ScheduleBase):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __str__(self):
        return f"{type(self).__name__}(value={self.value})"

    def get_value(self, step: int, total_steps: int) -> float:
        self._check_steps(step, total_steps)
        return self.value
