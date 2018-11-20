import json
import random
from typing import Dict, List, Tuple

from emoji.descriptions import EmojiDetails


# TODO(fabian): Now that we've library-fied the emoji stuff, we should get rid of the save/load
# thing.
def _load_data() -> Dict[int, List[EmojiDetails]]:
    with open('build/generated.json') as file:
        thingy = json.load(file)
        thingy = [EmojiDetails(*thing) for thing in thingy]
    wup: Dict[int, List[EmojiDetails]] = {}
    for item in thingy:
        for syllables in item.syllable_counts:
            if syllables not in wup:
                wup[syllables] = []
            wup[syllables].append(item)

    return wup


data = _load_data()


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
    emojis = " ".join(obj.emoji for obj in objs)
    descriptions = " ".join(obj.description.upper() for obj in objs)
    return emojis, descriptions


def haiku() -> Tuple[str, str]:
    haiku_lines = [_make_line(syllable_count) for syllable_count in [5, 7, 5]]
    emoji, desc = zip(*haiku_lines)
    return ("\n".join(emoji), "\n".join(desc))
