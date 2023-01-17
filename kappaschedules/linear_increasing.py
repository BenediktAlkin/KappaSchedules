from .base.increasing_progress_schedule import IncreasingProgressSchedule

from .functional.schedules import linear


class LinearIncreasing(IncreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return linear(step, total_steps)
