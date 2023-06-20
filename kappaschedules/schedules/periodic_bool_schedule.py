from .base import ScheduleBase


class PeriodicBoolSchedule(ScheduleBase):
    def __init__(self, initial_state, off_value=0., on_value=1., off_duration=1, on_duration=1, invert=False):
        super().__init__()
        self.initial_state = initial_state
        self.off_value = off_value
        self.on_value = on_value
        self.off_duration = off_duration
        self.on_duration = on_duration
        self.period_duration = off_duration + on_duration
        self.invert = invert

    def __str__(self):
        return (
            f"{type(self).__name__}"
            f"("
            f"intial_state={self.intial_state},"
            f"off_duration={self.off_duration},"
            f"on_duration={self.on_duration},"
            f"invert={self.invert}"
            f")"
        )

    def _get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        value = self._get_bool_value(step)
        if self.invert:
            return 1. - value
        return value

    def _get_bool_value(self, step: int) -> float:
        step_in_period = step % self.period_duration
        if self.initial_state:
            if step_in_period < self.on_duration:
                return self.on_value
            else:
                return self.off_value
        else:
            if step_in_period < self.off_duration:
                return self.off_value
            else:
                return self.on_value
