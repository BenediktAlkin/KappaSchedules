class ScheduleBase:
    def __init__(self, min_value=None):
        self.min_value = min_value
        # check that correct method is overwritten
        assert type(self).get_value == ScheduleBase.get_value

    def get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        assert 0 <= step < total_steps, f"0 <= step < total_steps (step={step} total_steps={total_steps})"
        value = self._get_value(step, total_steps, abs_step)
        if self.min_value is not None and value < self.min_value:
            return self.min_value
        return value

    def _get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError
