from typing import Iterable, NamedTuple

from bs4 import BeautifulSoup  # type: ignore


class EmojiAndDescription(NamedTuple):
    emoji: str
    description: str


def extract_emoji_pairs() -> Iterable[EmojiAndDescription]:
    with open('datasources/unicode-english.xml') as xmlfile:
        file = BeautifulSoup(xmlfile, 'html.parser')
        for annotation in file.annotations.find_all('annotation', type='tts'):
            yield EmojiAndDescription(annotation['cp'], annotation.string)
