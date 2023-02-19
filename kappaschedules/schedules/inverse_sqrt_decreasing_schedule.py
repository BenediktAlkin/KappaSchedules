from .base import DecreasingProgressSchedule
from .functional.schedules import inverse_sqrt


class InverseSqrtDecreasingSchedule(DecreasingProgressSchedule):
    def __init__(self, warmup_steps, **kwargs):
        super().__init__(**kwargs)
        self.warmup_steps = warmup_steps

    def _get_progress(self, step, total_steps):
        return 1 - inverse_sqrt(step, self.warmup_steps)
