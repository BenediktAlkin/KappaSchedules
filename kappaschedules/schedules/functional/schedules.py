import math


def linear(step, total_steps):
    """ linearly increasing from [0 to 1] """
    return step / max(1, total_steps - 1)


def cosine(step, total_steps):
    """ cosine schedule from [0 to 1] """
    progress = step / max(1, total_steps - 1)
    return 1 - (1 + math.cos(math.pi * progress)) / 2


def inverse_sqrt(step, warmup_steps):
    """ inverse square root schedule starting from 1 and going towards 0 """
    # https://github.com/facebookresearch/fairseq/blob/main/fairseq/optim/lr_scheduler/inverse_square_root_schedule.py
    return (step + warmup_steps) ** -0.5 * warmup_steps ** 0.5