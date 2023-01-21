from kappaschedules.base.increasing_progress_schedule import IncreasingProgressSchedule
from kappaschedules.functional.schedules import cosine


class CosineIncreasingSchedule(IncreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return cosine(step, total_steps)
