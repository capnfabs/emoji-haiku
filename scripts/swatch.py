import random
from typing import Iterable, List

from emoji.core import Emoji, Gender, Modifier, to_unicode_cps
from emoji.spec_parser import load_emoji_and_modifiers


def yield_lines(emoji: List[Emoji], mods: List[Modifier]) -> Iterable[str]:
    for e in emoji:
        modifier = random.choice(mods) if e.supports_modification else None
        gender = random.choice(list(Gender)) if e.supports_gender else Gender.NEUTRAL
        char = e.char(modifier=modifier, gender=gender)
        yield char + ' --> ' + to_unicode_cps(char)


def main():
    emoji, mods = load_emoji_and_modifiers()
    for swatch_line in yield_lines(emoji, mods):
        print(swatch_line)


if __name__ == '__main__':
    main()
