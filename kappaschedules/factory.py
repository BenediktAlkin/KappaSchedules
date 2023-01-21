import kappaschedules.schedules
from .schedules import SequentialStepSchedule, SequentialStepScheduleConfig
from .schedules.base import ScheduleBase
import inspect
from copy import deepcopy

def object_to_schedule(obj) -> ScheduleBase:
    if obj is None:
        return None
    if not isinstance(obj, (list, dict)):
        assert isinstance(obj, ScheduleBase)
        return obj

    if isinstance(obj, list):
        # sequential schedule
        schedule_configs = []
        for schedule_config in obj:
            assert isinstance(schedule_config, dict)
            assert "schedule" in schedule_config
            schedule = object_to_schedule(schedule_config["schedule"])
            schedule_configs.append(SequentialStepScheduleConfig(
                schedule=schedule,
                start_step=schedule_config.get("start_step", None),
                end_step=schedule_config.get("end_step", None),
            ))
        return SequentialStepSchedule(schedule_configs)

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
    return ctor(**obj)
