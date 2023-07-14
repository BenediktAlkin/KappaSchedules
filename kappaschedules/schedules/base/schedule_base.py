class ScheduleBase:
    def __init__(self):
        # check that correct method is overwritten
        assert type(self).get_value == ScheduleBase.get_value

    def get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        assert 0 <= step < total_steps, f"0 <= step < total_steps (step={step} total_steps={total_steps})"
        return self._get_value(step, total_steps, abs_step)

    def _get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError
