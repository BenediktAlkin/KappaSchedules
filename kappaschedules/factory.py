import kappaschedules.schedules
from .schedules import (
    SequentialPercentSchedule,
    SequentialPercentScheduleConfig,
    SequentialStepSchedule,
    SequentialStepScheduleConfig,
)
from .schedules.base import ScheduleBase
import inspect
from copy import deepcopy

def object_to_schedule(obj) -> ScheduleBase:
    if obj is None:
        return None
    if not isinstance(obj, (list, dict)):
        assert isinstance(obj, ScheduleBase)
        return obj

    # implicit sequential schedule
    if isinstance(obj, list):
        # check consistency between step/percent schedule
        step_counts = 0
        percent_counts = 0
        for schedule_config in obj:
            assert isinstance(schedule_config, dict)
            if "start_step" in schedule_config or "end_step" in schedule_config:
                step_counts += 1
            elif "start_percent" in schedule_config or "end_percent" in schedule_config:
                percent_counts += 1
        # if no start/end points are specified -> use step version
        if (step_counts == 0 and percent_counts == 0) or step_counts > 0:
            assert percent_counts == 0
            config_ctor = SequentialStepScheduleConfig
            ctor = SequentialStepSchedule
        elif percent_counts > 0:
            config_ctor = SequentialPercentScheduleConfig
            ctor = SequentialPercentSchedule
        else:
            raise NotImplementedError

        # sequential schedule
        schedule_configs = []
        for schedule_config in obj:
            assert "schedule" in schedule_config
            schedule = object_to_schedule(schedule_config["schedule"])
            kwargs = {k: v for k, v in schedule_config.items() if k != "schedule"}
            schedule_configs.append(config_ctor(schedule=schedule, **kwargs))
        return ctor(schedule_configs)

    # single schedules
    assert "kind" in obj and isinstance(obj["kind"], str)
    obj = deepcopy(obj)
    kind = obj.pop("kind")

    # get all names and ctors of schedules
    pascal_ctor_list = inspect.getmembers(kappaschedules.schedules, inspect.isclass)
    pascal_to_ctor = {name: ctor for name, ctor in pascal_ctor_list}
    # allow snake_case (type name is in PascalCase)
    if kind[0].islower:
        kind = kind.replace("_", "")
        snake_to_pascal = {name.lower(): name for name in pascal_to_ctor.keys()}
        assert kind in snake_to_pascal.keys(), f"invalid kind '{kind}' (possibilities: {snake_to_pascal.keys()})"
        kind = snake_to_pascal[kind]
    ctor = pascal_to_ctor[kind]

    # create SequentialScheduleConfig objects
    if ctor == SequentialPercentSchedule:
        obj["schedule_configs"] = _obj_to_schedule_configs(obj["schedule_configs"], SequentialPercentScheduleConfig)
    elif ctor == SequentialStepSchedule:
        obj["schedule_configs"] = _obj_to_schedule_configs(obj["schedule_configs"], SequentialStepScheduleConfig)

    return ctor(**obj)

def _obj_to_schedule_configs(obj, config_ctor):
    schedule_configs = []
    for schedule_config in obj:
        schedule = object_to_schedule(schedule_config.pop("schedule"))
        schedule_configs.append(config_ctor(schedule=schedule, **schedule_config))
    return schedule_configs