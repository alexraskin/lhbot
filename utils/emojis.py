import random


def random_emoji():
    """
    The random_emoji function is used to randomly select an emoji from the list of emojis.
    The random_emoji function does not take any arguments and returns a string.

    :return: a random emoji from the list.
    """
    emoji_list = [
        "😁",
        "🥶",
        "👌",
        "👀",
        "🤖",
        "👽",
        "💀",
        "🤯",
        "🤠",
        "📼",
        "📈",
        "🧡",
        "✨",
        "🍑",
        "🔨",
        "🛡️",
        "🇫🇮",
        "🐸",
        "🐈",
        "✨",
    ]
    return random.choice(list(emoji_list))
