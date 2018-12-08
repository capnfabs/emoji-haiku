from typing import Iterable, NamedTuple, Tuple

from bs4 import BeautifulSoup  # type: ignore

from emoji import spec_parser
from emoji.core import Emoji, Gender, GenderMode


class EmojiAndDescription(NamedTuple):
    emoji: str
    description: str


def _load_cps_and_tts_from_file() -> Iterable[EmojiAndDescription]:
    with open('datasources/unicode-english.xml') as xmlfile:
        file = BeautifulSoup(xmlfile, 'html.parser')
        for annotation in file.annotations.find_all('annotation', type='tts'):
            yield EmojiAndDescription(annotation['cp'], annotation.string)


def load_emoji_description_pairs() -> Iterable[Tuple[Emoji, str]]:
    cp_to_tts = dict(_load_cps_and_tts_from_file())
    emojis, _ = spec_parser.load_emoji_and_modifiers()
    e: Emoji
    for e in emojis:
        if e.gender_mode == GenderMode.OBJECT_FORMAT:
            # Gotta do something tricky.
            # Might have presentation chars
            f_char = e.char(gender=Gender.FEMININE)
            m_char = e.char(gender=Gender.MASCULINE)
            if e.defaults_to_text:
                # Have to remove the emoji presentation selector so that it can be looked up :-/
                f_char = f_char[:-1]
                m_char = m_char[:-1]

            f_desc = cp_to_tts[f_char]
            m_desc = cp_to_tts[m_char]

            assert f_desc.startswith('woman ') and m_desc.startswith('man ')
            f_role = f_desc[6:]
            m_role = m_desc[4:]
            assert f_role == m_role
            yield e, f_role
        else:
            # Just look up as-is. Note that there's a single character '🔟' that doesn't appear to
            # be represented in the CLDR source right now, which is why this conditional exists.
            if e.base_char in cp_to_tts:
                yield e, cp_to_tts[e.base_char]
