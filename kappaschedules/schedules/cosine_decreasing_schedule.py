from kappaschedules.base.decreasing_progress_schedule import DecreasingProgressSchedule
from kappaschedules.functional.schedules import cosine


class CosineDecreasingSchedule(DecreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return cosine(step, total_steps)
