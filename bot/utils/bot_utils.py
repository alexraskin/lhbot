import time
from datetime import datetime


def get_year_string() -> str:
    now = datetime.utcnow()
    year_end = datetime(now.year + 1, 1, 1)
    year_start = datetime(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return f"For your information, the year is {year_percent:.1f}% over!"


def get_year_round() -> str:
    now = datetime.utcnow()
    year_end = datetime(now.year + 1, 1, 1)
    year_start = datetime(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return year_percent


def get_time_string() -> str:
    return datetime.utcnow().__str__()


def progress_bar(percent):
    bar_filled = "▓"
    bar_empty = "░"
    length = 15

    progress_bar = bar_filled * int((percent / (100.0 / length)))
    progress_bar += bar_empty * (length - len(progress_bar))
    return f"{progress_bar} {percent:.1f}%"


def date(target, clock: bool = True, ago: bool = False, only_ago: bool = False) -> str:
    """Converts a timestamp to a Discord timestamp format"""
    if isinstance(target, int) or isinstance(target, float):
        target = datetime.utcfromtimestamp(target)

    unix = int(time.mktime(target.timetuple()))
    timestamp = f"<t:{unix}:{'f' if clock else 'D'}>"
    if ago:
        timestamp += f" (<t:{unix}:R>)"
    if only_ago:
        timestamp = f"<t:{unix}:R>"
    return timestamp
