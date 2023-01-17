import math


def linear(step, total_steps):
    """ linearly increasing from [0 to 1] """
    return step / max(1, total_steps - 1)


def cosine(step, total_steps):
    """ cosine schedule from [0 to 1] """
    progress = step / max(1, total_steps - 1)
    return 1 - (1 + math.cos(math.pi * progress)) / 2
