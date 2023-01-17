from kappaschedules.base.schedule_base import ScheduleBase

class DummySchedule(ScheduleBase):
    def get_value(self, step: int, total_steps: int) -> float:
        return 0.

    def __str__(self):
        return "Dummy"