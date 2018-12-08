"""Methods for counting the number of syllables in a string."""
import re
from collections import defaultdict
from typing import Dict, Iterable, Set

# TODO: document this.
_OVERRIDES = {
    '1ST': 1,
    '2ND': 2,
    '3': 1,
    '3RD': 1,
    '8': 1,
    'AB': 2,
    'ALEMBIC': 3,
    'CABLEWAY': 3,
    'CARTWHEELING': 3,
    'CHEQUERED': 2,
    'CITYSCAPE': 3,
    'CL': 2,
    'CLINKING': 2,
    'DIVIDERS': 3,
    'FACEPALMING': 3,
    'FLATBREAD': 2,
    'GIBBOUS': 2,
    'HEADSCARF': 2,
    'HIBISCUS': 3,
    'INBOX': 2,
    'KAABA': 2,
    'LOWERCASE': 3,
    # Weird that this isn't in the dict, but 'MAGES' is.
    'MAGE': 1,
    'MAHJONG': 2,
    'MANTELPIECE': 3,
    'MERIDIANS': 4,
    'MERPERSON': 3,
    # I guess?
    'MOAI': 2,
    'MOTORWAY': 3,
    'NOTEPAD': 2,
    'OM': 1,
    'OPHIUCHUS': 4,
    'OUTBOX': 2,
    'PAPERCLIP': 3,
    'PAPERCLIPS': 3,
    'POSTBOX': 2,
    'PUSHPIN': 2,
    'SAGITTARIUS': 5,
    'SAKE': 2,
    'SAUROPOD': 3,
    'SHUSHING': 2,
    # Maybe 3? spar-ker-ler
    'SPARKLER': 2,
    'SPLAYED': 1,
    'SPOKED': 1,
    'SUPERVILLAIN': 4,
    'TANABATA': 4,
    'TRAMWAY': 2,
    'TROLLEYBUS': 3,
    'UNAMUSED': 3,
    'UPPERCASE': 3,
    'ZZZ': 1,
}


def _load_vowels() -> Iterable[str]:
    with open('datasources/cmudict/cmudict-0.7b.phones.txt') as key:
        for line in key:
            sound, sound_type = line.split()
            if sound_type == 'vowel':
                yield sound


def _load_syllables_per_word_cmu() -> Dict[str, Set[int]]:
    vowels = set(_load_vowels())
    dataset: Dict[str, Set[int]] = defaultdict(lambda: set())

    regex = re.compile(r'(?P<word>.*)\(\d+\)')

    with open('datasources/cmudict/cmudict-0.7b.txt') as file:
        for line in file:
            if line.startswith(';;;'):
                # ignore
                continue

            row = line.split()
            word_and_variant, *sounds = row
            num_syllables = sum(1 for sound in sounds if sound.rstrip('0123456789') in vowels)

            match = regex.fullmatch(word_and_variant)
            word = match['word'] if match else word_and_variant

            counts = dataset[word]

            counts.add(num_syllables)

    # Convert to dict, because now that we've done the data processing, we want this to throw
    # KeyErrors if it can't find a word.
    return dict(dataset)


def _apply_overrides(
        source_dict: Dict[str, Set[int]], overrides: Dict[str, int]) -> Dict[str, Set[int]]:
    # Make a copy
    source_dict = dict(source_dict)

    for key, val in overrides.items():
        source_dict[key] = {val}

    return source_dict


_source_dict = _apply_overrides(_load_syllables_per_word_cmu(), _OVERRIDES)


def count_syllables(input: str) -> Set[int]:
    """Returns a set, where each item is a syllable count of a possible pronunciation of `input`."""

    cleaned = _clean_text(input)
    # Split input text based on whitespace and dashes (because hypenated words don't often appear
    # in the pronunciation dict).
    words = re.split(r'[\s-]', cleaned)
    input.split(' ')
    totals = {0}
    for word in words:
        word_counts = _source_dict[word]
        totals = {t + wc for t in totals for wc in word_counts}

    return totals


# Here are all the non-letter characters we're keeping:
# - Dashes and spaces - we should split on these later
# - single quotes - so we can look up words like O'CLOCK
# - numbers - because words like 1ST and 2ND should be handled.
_remove_weird_symbols = re.compile(r"[^a-zA-Z\d\-\s']")


def _clean_text(word: str) -> str:
    """Cleans weird / disallowed symbols from a string, and standardises to uppercase."""
    # Yep, smart quotes.
    word = word.replace('’', "'")
    word = word.upper()
    return _remove_weird_symbols.sub('', word)
