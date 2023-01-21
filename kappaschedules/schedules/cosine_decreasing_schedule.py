from .base import DecreasingProgressSchedule
from .functional.schedules import cosine


class CosineDecreasingSchedule(DecreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return cosine(step, total_steps)
