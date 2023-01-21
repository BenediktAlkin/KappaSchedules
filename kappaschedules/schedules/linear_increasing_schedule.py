from .base import IncreasingProgressSchedule

from .functional.schedules import linear


class LinearIncreasingSchedule(IncreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return linear(step, total_steps)
