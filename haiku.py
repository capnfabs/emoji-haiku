import random
from typing import Dict, Iterable, List, Tuple

from emoji import descriptions, spec_parser
from emoji.core import Emoji, Gender, Modifier
from syllables import count_syllables


def _load_resources() -> Tuple[Dict[Emoji, str], List[Modifier]]:
    emojis, modifier_list = spec_parser.load_emoji_and_modifiers()
    modifiers = list(modifier_list)

    emoji_descriptions = list(descriptions.load_descriptions_for_emojis(emojis))

    # Filter out anything where we couldn't load the description
    emojis_to_descriptions = {e: d for e, d in zip(emojis, emoji_descriptions) if d is not None}

    return emojis_to_descriptions, modifiers


def _map_description_to_emoji_and_syllable_count(
        emoji_desc_pairs: Iterable[Tuple[Emoji, str]]) -> Dict[int, List[Tuple[Emoji, str]]]:
    # TODO: commenting this is hard but probably worthwhile because this code is mad confusing.
    return_dict: Dict[int, List[Tuple[Emoji, str]]] = {}
    for emoji, desc in emoji_desc_pairs:
        syllable_options = count_syllables(desc)
        for syllable_count in syllable_options:
            list_for_syllable_count = return_dict.get(syllable_count, [])
            list_for_syllable_count.append((emoji, desc))
            return_dict[syllable_count] = list_for_syllable_count
    return return_dict


emojis_to_descriptions, modifiers = _load_resources()


data = _map_description_to_emoji_and_syllable_count(emojis_to_descriptions.items())


def _make_line(syllable_count: int) -> Tuple[str, str]:
    # choose a syllable length probability
    syllables_per_emoji: List[int] = []
    while sum(syllables_per_emoji) < syllable_count:
        # This feels hard to read. fix this.
        # The idea is - weight longer emojis in proportion to lengths.
        allowable_sets = sorted(
            (k, v) for k, v in data.items()
            if k <= syllable_count - sum(syllables_per_emoji))
        keys, _ = zip(*allowable_sets)
        elements = random.choices(keys, weights=[key * len(val) for key, val in allowable_sets])
        syllables_per_emoji.append(*elements)

    objs = list(random.choice(data[syll]) for syll in syllables_per_emoji)
    chosen_emojis = (obj[0] for obj in objs)
    emojis = " ".join(_render_emoji(emoji) for emoji in chosen_emojis)
    descriptions = " ".join(obj[1].upper() for obj in objs)
    return emojis, descriptions


def _render_emoji(emoji: Emoji) -> str:
    modifier = random.choice(modifiers) if emoji.supports_modification else None
    gender = random.choice(
        [Gender.MASCULINE, Gender.FEMININE]) if emoji.supports_gender else Gender.NEUTRAL
    return emoji.char(modifier=modifier, gender=gender)


def haiku() -> Tuple[str, str]:
    haiku_lines = [_make_line(syllable_count) for syllable_count in [5, 7, 5]]
    emoji, desc = zip(*haiku_lines)
    return ("\n".join(emoji), "\n".join(desc))
