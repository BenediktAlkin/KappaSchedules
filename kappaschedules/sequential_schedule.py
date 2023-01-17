from kappaschedules.base.schedule_base import ScheduleBase
from dataclasses import dataclass
from typing import List

@dataclass
class SequentialScheduleConfig:
    schedule: ScheduleBase
    start_step: int = None
    end_step: int = None


class SequentialSchedule(ScheduleBase):
    def __init__(self, schedule_configs: List[SequentialScheduleConfig]):
        super().__init__()
        assert len(schedule_configs) > 0
        self.schedule_configs = schedule_configs

        # if first schedule has no start_step -> set to 0 -> this ensures every schedule has a start_step
        if schedule_configs[0].start_step is None:
            schedule_configs[0].start_step = 0
        # propagate start/end
        for i in range(1, len(schedule_configs) - 1):
            # take start_step from previous schedule
            if schedule_configs[i].start_step is None:
                schedule_configs[i].start_step = schedule_configs[i - 1].end_step
            # take end_step from next schedule
            if schedule_configs[i].end_step is None:
                schedule_configs[i].end_step = schedule_configs[i + 1].start_step
        # edge case: last schedule propagate
        if len(schedule_configs) > 1:
            # propagate [-2].end_step forward
            if schedule_configs[-1].start_step is None:
                schedule_configs[-1].start_step = schedule_configs[-2].end_step
            # propagate [-1].start_step backward
            if schedule_configs[-2].end_step is None:
                schedule_configs[-2].end_step = schedule_configs[-1].start_step

        # check correctness of start/end
        if len(schedule_configs) == 1:
            # edge case: single schedule
            # always: 0 <= start
            # if end is not None: start <= end
            assert 0 <= schedule_configs[0].start_step
            if schedule_configs[0].end_step is not None:
                assert schedule_configs[0].start_step <= schedule_configs[0].end_step
        else:
            # check 0 <= cfg[i].start <= cfg[i].end
            # check cfg[i].end <= cfg[i+1].start
            for i in range(len(schedule_configs) - 1):
                assert schedule_configs[i].start_step is not None and schedule_configs[i].end_step is not None
                assert 0 <= schedule_configs[i].start_step <= schedule_configs[i].end_step
                assert schedule_configs[i].end_step <= schedule_configs[i + 1].start_step
            # last schedule is allowed to have no end_step
            if schedule_configs[-1].end_step is None:
                assert 0 <= schedule_configs[-1].start_step
            else:
                assert 0 <= schedule_configs[-1].start_step <= schedule_configs[-1].end_step

    def get_sequential_schedule_config(self, step: int) -> SequentialScheduleConfig:
        # step < config[0].start_step -> None
        # config[-1].end_step < step -> config[-1]
        for i in reversed(range(len(self.schedule_configs))):
            if self.schedule_configs[i].start_step <= step:
                return self.schedule_configs[i]
        return None

    def get_value(self, step: int, total_steps: int) -> float:
        config = self.get_sequential_schedule_config(step)
        if config is None:
            raise NotImplementedError
        return config.schedule.get_value(step, total_steps)

    def __str__(self):
        raise NotImplementedError
