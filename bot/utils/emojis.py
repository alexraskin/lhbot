import random


def random_emoji() -> str:
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
