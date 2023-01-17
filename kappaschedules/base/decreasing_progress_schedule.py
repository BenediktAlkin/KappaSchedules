from .progress_schedule import ProgressSchedule


class DecreasingProgressSchedule(ProgressSchedule):
    def __init__(self, abs_max_value=1., abs_end_value=0., **kwargs):
        delta = abs_end_value - abs_max_value
        assert delta <= 0.
        super().__init__(abs_start_value=abs_max_value, abs_delta=delta, **kwargs)

    def _get_progress(self, step, total_steps):
        raise NotImplementedError
