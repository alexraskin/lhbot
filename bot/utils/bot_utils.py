from datetime import datetime as dt


def get_year_string() -> str:
    """
    The get_year_string function is used to get the current year and then
    calculate the percentage of time that has passed in relation to the total
    number of days in a year. This is done by taking today's date, adding one
    year and subtracting today's date from that new date. Then dividing this
    difference by 365 (the number of days in a year) and multiplying it by 100.

    :return: the percentage of the current year that has elapsed.
    """
    now = dt.utcnow()
    year_end = dt(now.year + 1, 1, 1)
    year_start = dt(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return f"For your information, the year is {year_percent:.1f}% over!"


def get_time_string() -> str:
    """
    The get_time_string function is used to get the current time
    :return: The current time in the form of a string
    """
    return dt.utcnow().__str__()
