import math

from .base.increasing_progress_schedule import IncreasingProgressSchedule


class LinearIncreasing(IncreasingProgressSchedule):
    def _get_value(self, step, total_steps):
        progress = step / max(1, total_steps - 1)
        return progress
