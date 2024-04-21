class ScheduleBase:
    def __init__(self, overhang_percent=None, overhang_steps=None):
        # schedule is artificially prolonged
        assert overhang_percent is None or overhang_steps is None, \
            f"overhang_percent and overhang_steps are mutually exclusive"
        self.overhang_percent = overhang_percent
        self.overhang_steps = overhang_steps
        # check that correct method is overwritten
        assert type(self).get_value == ScheduleBase.get_value

    def get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        assert 0 <= step < total_steps, f"0 <= step < total_steps (step={step} total_steps={total_steps})"
        if self.overhang_percent is not None:
            total_steps += int(total_steps * self.overhang_percent)
        if self.overhang_steps is not None:
            total_steps += self.overhang_steps
        return self._get_value(step, total_steps, abs_step)

    def _get_value(self, step: int, total_steps: int, abs_step: int = None) -> float:
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError
