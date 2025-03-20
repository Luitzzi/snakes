import random
import time


def get_time_ms():
    return time.time() * 1000


def get_random_time(time_range):
    return random.randint(time_range[0], time_range[1])
