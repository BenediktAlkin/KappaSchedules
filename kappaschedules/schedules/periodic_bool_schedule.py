from .base import ScheduleBase


class PeriodicBoolSchedule(ScheduleBase):
    def __init__(self, initial_state, off_duration=1, on_duration=1):
        super().__init__()
        self.initial_state = initial_state
        self.off_duration = off_duration
        self.on_duration = on_duration
        self.period_duration = off_duration + on_duration

    def __str__(self):
        return (
            f"{type(self).__name__}"
            f"("
            f"intial_state={self.intial_state},"
            f"off_duration={self.off_duration},"
            f"on_duration={self.on_duration}"
            f")"
        )

    def _get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        step_in_period = step % self.period_duration
        if self.initial_state:
            if step_in_period < self.on_duration:
                return 1.
            else:
                return 0.
        else:
            if step_in_period < self.off_duration:
                return 0.
            else:
                return 1.
