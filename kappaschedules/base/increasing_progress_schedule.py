from .progress_schedule import ProgressSchedule


class IncreasingProgressSchedule(ProgressSchedule):
    def __init__(self, abs_start_value=0., abs_max_value=1., **kwargs):
        delta = abs_max_value - abs_start_value
        assert delta >= 0.
        super().__init__(abs_start_value=abs_start_value, abs_delta=delta, **kwargs)

    def _get_progress(self, step, total_steps):
        raise NotImplementedError
