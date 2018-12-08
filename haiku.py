import random
from typing import Dict, Iterable, List, Tuple

from emoji import descriptions, spec_parser
from emoji.core import Emoji, Gender, Modifier
from syllables import count_syllables


def _load_resources() -> Tuple[Dict[Emoji, str], List[Modifier]]:
    """Loads emojis and descriptions."""

    emojis, modifier_list = spec_parser.load_emoji_and_modifiers()
    modifiers = list(modifier_list)

    emoji_descriptions = list(descriptions.load_descriptions_for_emojis(emojis))

    # Filter out anything where we couldn't load the description
    emojis_to_descriptions = {e: d for e, d in zip(emojis, emoji_descriptions) if d is not None}

    return emojis_to_descriptions, modifiers


def _map_description_to_emoji_and_syllable_count(
        emoji_desc_pairs: Iterable[Tuple[Emoji, str]]) -> Dict[int, List[Tuple[Emoji, str]]]:
    """Takes a list of [Emoji, description] pairs and maps them to a dict of format:
        [syllable count] --> A list of all [emoji, description] pairs where the description has that
                             syllable count.
    """

    return_dict: Dict[int, List[Tuple[Emoji, str]]] = {}

    for emoji, desc in emoji_desc_pairs:
        syllable_options = count_syllables(desc)
        for syllable_count in syllable_options:
            list_for_syllable_count = return_dict.get(syllable_count, [])
            list_for_syllable_count.append((emoji, desc))
            return_dict[syllable_count] = list_for_syllable_count
    return return_dict


_emojis_to_descriptions, modifiers = _load_resources()
_data = _map_description_to_emoji_and_syllable_count(_emojis_to_descriptions.items())


def _make_line(syllable_count: int) -> Tuple[str, str]:
    """Make a Haiku line with the given number of syllables.
    Returns a Tuple of (emoji representation, text representation).
    """
    syllables_per_emoji: List[int] = []

    # This logic is complicated, but here's what it's doing:
    # - On each iteration, filter out entries that have a too-high syllable count
    # - Choose a 'number of syllables' based on what's left. The 'number of syllables' that we
    #   choose is weighted such that the end result is "Each emoji has a chance of being selected
    #   proportional to its syllable count". That is, emojis with longer descriptions are given
    #   preference.
    # The rationale for the weighting is that we want the longer emojis to still be displayed with
    # some regularity, and so we give them a helping hand by doing this.
    while sum(syllables_per_emoji) < syllable_count:
        # This is an iterable of (allowable syllables, List[possible emoji/desc pairs])
        # This specific operation is removing all possible choices
        allowable_syllables = sorted(
            (k, v) for k, v in _data.items()
            if k <= syllable_count - sum(syllables_per_emoji))

        keys, _ = zip(*allowable_syllables)
        elements = random.choices(
            keys, weights=[key * len(val) for key, val in allowable_syllables])
        syllables_per_emoji.append(*elements)

    # Choose emojis for the given syllable count
    objs = list(random.choice(_data[syll]) for syll in syllables_per_emoji)
    chosen_emojis = (emoji for emoji, desc in objs)

    # Format and return.
    emojis = " ".join(_render_emoji(emoji) for emoji in chosen_emojis)
    descriptions = " ".join(desc.upper() for emoji, desc in objs)
    return emojis, descriptions


def _render_emoji(emoji: Emoji) -> str:
    """Render an Emoji into unicode, randomly applying skin color modifiers and gender.
    """
    modifier = random.choice(modifiers) if emoji.supports_modification else None
    # Don't use neutral gender, even if available on an emoji, because part of the reason why the
    # genders were added to unicode were because things were previously pretty heavily gender-coded.
    gender = random.choice(
        [Gender.MASCULINE, Gender.FEMININE]) if emoji.supports_gender else Gender.NEUTRAL
    return emoji.char(modifier=modifier, gender=gender)


def haiku() -> Tuple[str, str]:
    """Generates a Haiku. Returns a tuple, where:
    - First element is an emoji representation. Each line in the Haiku is separated by a '\n'.
    - Second element is a textual representation.
    """
    haiku_lines = [_make_line(syllable_count) for syllable_count in [5, 7, 5]]
    emoji, desc = zip(*haiku_lines)
    return "\n".join(emoji), "\n".join(desc)
