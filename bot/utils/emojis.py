import random


def random_emoji():
    """
    The random_emoji function is used to randomly select an emoji from the list of emojis.
    The random_emoji function does not take any arguments and returns a string.

    :return: a random emoji from the list.
    """
    emoji_list = [
        "๐",
        "๐ฅถ",
        "๐",
        "๐",
        "๐ค",
        "๐ฝ",
        "๐",
        "๐คฏ",
        "๐ค ",
        "๐ผ",
        "๐",
        "๐งก",
        "โจ",
        "๐",
        "๐จ",
        "๐ก๏ธ",
        "๐ซ๐ฎ",
        "๐ธ",
        "๐",
        "โจ",
    ]
    return random.choice(list(emoji_list))
