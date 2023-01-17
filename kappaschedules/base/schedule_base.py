class ScheduleBase:
    @staticmethod
    def _check_steps(step, total_steps):
        assert 0 <= step < total_steps, f"0 <= step < total_steps (step={step} total_steps={total_steps})"

    def get_value(self, step, total_steps):
        raise NotImplementedError

    def __repr__(self):
        return str(self)

    def __str__(self):
        raise NotImplementedError
