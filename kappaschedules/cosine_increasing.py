from .base.increasing_progress_schedule import IncreasingProgressSchedule
from .functional import cosine


class CosineIncreasing(IncreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return cosine(step, total_steps)
