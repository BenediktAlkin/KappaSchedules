from .base.decreasing_progress_schedule import DecreasingProgressSchedule

from .functional.schedules import linear


class LinearDecreasing(DecreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return linear(step, total_steps)
