from kappaschedules.base.decreasing_progress_schedule import DecreasingProgressSchedule

from kappaschedules.functional.schedules import linear


class LinearDecreasingSchedule(DecreasingProgressSchedule):
    def _get_progress(self, step, total_steps):
        return linear(step, total_steps)
