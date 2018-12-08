from typing import Iterable, NamedTuple, Optional

from bs4 import BeautifulSoup  # type: ignore

from emoji.core import Emoji, Gender, GenderMode


class EmojiAndDescription(NamedTuple):
    emoji: str
    description: str


def _load_cps_and_tts_from_file() -> Iterable[EmojiAndDescription]:
    with open('datasources/unicode-english.xml') as xmlfile:
        file = BeautifulSoup(xmlfile, 'html.parser')
        for annotation in file.annotations.find_all('annotation', type='tts'):
            yield EmojiAndDescription(annotation['cp'], annotation.string)


def load_descriptions_for_emojis(emojis: Iterable[Emoji]) -> Iterable[Optional[str]]:
    """Loads descriptions for the given emojis. If a description couldn't be loaded, 'None' is used.
    """
    cp_to_tts = dict(_load_cps_and_tts_from_file())
    for e in emojis:
        if e.gender_mode == GenderMode.OBJECT_FORMAT:
            # For OBJECT FORMAT, we want to grab a gender-neutral label. The labels are all of the
            # form "[woman/man] [noun]", e.g. "woman scientist", "man scientist", which we want to
            # just transform to "[noun]".

            # Render the woman / man gendered versions
            f_char = e.char(gender=Gender.FEMININE)
            m_char = e.char(gender=Gender.MASCULINE)

            # The CLDR spec leaves off the emoji presentation selector, but our rendering code
            # always adds the presentation selector. So we sorta 'reverse engineer' that here and
            # strip off the presentation selector so that the lookup succeeds.
            if e.defaults_to_text:
                f_char = f_char[:-1]
                m_char = m_char[:-1]

            f_desc = cp_to_tts[f_char]
            m_desc = cp_to_tts[m_char]

            assert f_desc.startswith('woman ') and m_desc.startswith('man ')
            # trim off the 'woman' and 'man' to get the gender-neutral noun.
            f_role = f_desc[6:]
            m_role = m_desc[4:]
            assert f_role == m_role
            yield f_role
        else:
            # Just look up as-is. Note that there's a single character '🔟' that doesn't appear to
            # be represented in the CLDR source right now, which is why this conditional exists.
            if e.base_char in cp_to_tts:
                yield cp_to_tts[e.base_char]
