from datetime import datetime as dt


def get_year_string() -> str:
    now = dt.utcnow()
    year_end = dt(now.year + 1, 1, 1)
    year_start = dt(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return f"For your information, the year is {year_percent:.1f}% over!"


def get_year_round() -> str:
    now = dt.utcnow()
    year_end = dt(now.year + 1, 1, 1)
    year_start = dt(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return year_percent


def get_time_string() -> str:
    return dt.utcnow().__str__()


def progress_bar(percent):
    bar_filled = "▓"
    bar_empty = "░"
    length = 15

    progress_bar = bar_filled * int((percent / (100.0 / length)))
    progress_bar += bar_empty * (length - len(progress_bar))
    return f"{progress_bar} {percent:.1f}%"
