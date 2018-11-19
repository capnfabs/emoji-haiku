from bs4 import BeautifulSoup  # type: ignore
from typing import NamedTuple, List, Iterable, Dict, Set
import re
from collections import defaultdict
import itertools
import json
import os

class EmojiAndDescription(NamedTuple):
    emoji: str
    description: str

class EmojiDetails(NamedTuple):
    emoji: str
    description: str
    syllable_counts: List[int]

def extract_emoji_pairs() -> Iterable[EmojiAndDescription]:
    with open('datasources/unicode-english.xml') as xmlfile:
        file = BeautifulSoup(xmlfile, 'html.parser')
        for annotation in file.annotations.find_all('annotation', type='tts'):
            yield EmojiAndDescription(annotation['cp'], annotation.string)


def _load_vowels() -> Iterable[str]:
    with open('datasources/cmudict-0.7b.phones.txt') as key:
        for line in key:
            sound, sound_type = line.split()
            if sound_type == 'vowel':
                yield sound


def load_pronunciations() -> Dict[str, Set[int]]:
    vowels = set(_load_vowels())
    dataset: Dict[str, Set[int]] = defaultdict(lambda: set())
    
    regex = re.compile(r'(?P<word>.*)\(\d+\)')

    with open('datasources/cmudict-0.7b.txt') as file:
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

    return dataset

# This keeps dashes, single quotes, and numbers. They're explicitly allowed.
_remove_weird_symbols = re.compile(r"[^a-zA-Z\d\-']")

OVERRIDES = {
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
    'SAKE': 1,
    'SAUROPOD': 3,
    'SHUSHING': 2,
    # Maybe 3?
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

def adjust_word(word: str) -> List[str]:
     # Yep, smart quotes.
    word = word.replace('’', "'")
    word = word.upper()
    word = _remove_weird_symbols.sub('', word)
    return word.split('-')


def count_syllables(words: List[str], source_dict: Dict[str, Set[int]]) -> Set[int]:
    # A set with just the value 0 in it
    totals = {0}
    for word in words:
        word_counts = source_dict[word]
        totals = {t + wc for t in totals for wc in word_counts}

    return totals

def merged_results() -> Iterable[EmojiDetails]:
    pronunciations = load_pronunciations()

    # Add the overrides
    for key, val in OVERRIDES.items():
        pronunciations[key] = {val}

    # compute the data
    for emoji in extract_emoji_pairs():
        words = emoji.description.split()
        words = list(w for ws in words for w in adjust_word(ws))
        options = count_syllables(words, pronunciations)

        yield EmojiDetails(emoji.emoji, emoji.description, list(options))

def write_results_to_json(filename: str) -> None:
    data = list(merged_results())
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

def main() -> None:
    # TODO: this JSON is ugly, and might be nicer as a dict?
    os.makedirs('build')
    write_results_to_json('build/generated.json')

if __name__ == '__main__':
    main()
