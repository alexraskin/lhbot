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
    return  f"{year_percent:.1f}"

def get_year_round() -> str:
    now = dt.utcnow()
    year_end = dt(now.year + 1, 1, 1)
    year_start = dt(now.year, 1, 1)
    year_percent = (now - year_start) / (year_end - year_start) * 100
    return year_percent

def get_time_string() -> str:
    """
    The get_time_string function is used to get the current time
    :return: The current time in the form of a string
    """
    return dt.utcnow().__str__()

def progress_bar(percent):
    """
    The progress_bar function prints a progress bar to the console.
    
    :param percent: Display the percentage of completion
    :return: A string that represents a progress bar
    """
    bar_filled = '▓'
    bar_empty = '░'
    length = 15

    progress_bar = bar_filled * int((percent / (100. / length)))
    progress_bar += bar_empty * (length - len(progress_bar))
    return f'{progress_bar} {percent:.1f}%'
