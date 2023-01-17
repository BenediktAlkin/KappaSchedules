from .base.decreasing_progress_schedule import DecreasingProgressSchedule
from .functional import cosine


class CosineDecreasing(DecreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return cosine(step, total_steps)
