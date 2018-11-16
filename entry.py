from descriptions import EmojiDetails
from collections import defaultdict
from typing import List, Dict, Tuple
import json
import random

def load_data() -> Dict[int, List[EmojiDetails]]:
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

data = load_data()

def make_line(syllable_count: int) -> Tuple[str, str]:
    # choose a syllable length probability
    syllables_per_emoji: List[int] = []
    while sum(syllables_per_emoji) < syllable_count:
        # This feels hard to read. fix this.
        # The idea is - weight longer emojis in proportion to lengths.
        allowable_sets = sorted((k, v) for k, v in data.items() if k <= syllable_count - sum(syllables_per_emoji))
        keys, _ = zip(*allowable_sets)
        elements = random.choices(keys, weights=[key * len(val) for key, val in allowable_sets])
        syllables_per_emoji.append(*elements)

    objs = list(random.choice(data[syll]) for syll in syllables_per_emoji)
    emojis = " ".join(obj.emoji for obj in objs)
    descriptions = " ".join(obj.description.upper() for obj in objs)
    return emojis, descriptions

def haiku() -> Tuple[str, str]:
    haiku_lines = [make_line(syllable_count) for syllable_count in [5, 7, 5]]
    emoji, desc = zip(*haiku_lines)
    return ("\n".join(emoji), "\n".join(desc))

