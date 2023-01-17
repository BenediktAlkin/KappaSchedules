from .schedule_base import ScheduleBase


class ProgressSchedule(ScheduleBase):
    def __init__(self, abs_start_value, abs_delta, exclude_first=False, exclude_last=False):
        self.abs_start_value = abs_start_value
        self.abs_delta = abs_delta
        self.exclude_first = exclude_first
        self.exclude_last = exclude_last

    def __str__(self):
        return (
            f"{type(self).__name__}("
            f"start={self.abs_start_value}, "
            f"end={self.abs_start_value + self.abs_delta}, "
            f"excl_first={self.exclude_first}, "
            f"excl_last={self.exclude_last}"
            f")"
        )

    def get_value(self, step, total_steps):
        self._check_steps(step, total_steps)
        if self.exclude_last:
            total_steps += 1
        if self.exclude_first:
            step += 1
            total_steps += 1
        # get value from schedule (in [0, 1])
        value = self._get_value(step, total_steps)
        # adjust to "absolute value" (i.e. real learning rate)
        value = self.abs_start_value + value * self.abs_delta
        return value

    def _get_value(self, step, total_steps):
        raise NotImplementedError
