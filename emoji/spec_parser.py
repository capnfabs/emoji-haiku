"""Methods for parsing the unicode spec, and retrieving a list of Emoji and Modifiers.

Note that the model of 'Emoji' here isn't sufficiently general to represent everything in the spec -
a visual / user-facing emoji could be, for example, a super complicated Zero-Width-Join sequence. I
wanted to go in favor of ease-of-use instead of comprehensiveness here, though, so there are some
emoji that aren't represented.

An important part of this module is emoji_unicode_11_manual_supplement.py. This is a manual
interpretation of a lot of the data in the emoji-zwj-sequences.txt file, based on my reading of The
Spec.
"""
import os
from collections import defaultdict
from typing import Dict, Iterable, List, NamedTuple, Optional, Set, Tuple

import emoji.emoji_unicode_11_manual_supplement as supplement
from emoji.core import Emoji, GenderMode, Modifier


class EmojiData(NamedTuple):
    emojis: List[Emoji]
    modifiers: List[Modifier]


# A Unicode code point, as defined by the Unicode spec. This is just an int; the type only exists to
# provide a way of documenting return types more precisely.
_CodePoint = int


class _CodePointInfo(NamedTuple):
    classes: Set[str]
    comments: Set[str]


def _make_cpi() -> _CodePointInfo:
    return _CodePointInfo(set(), set())


def _load_codepoints(data_directory: str) -> Dict[_CodePoint, _CodePointInfo]:
    """Returns a Dict mapping every possible emoji character to information known about it, from the
    unicode data specification.
    """
    result: Dict[_CodePoint, _CodePointInfo] = defaultdict(_make_cpi)
    for codepoint_or_range, codepoint_class, comment in _scan_codepoints_file(data_directory):
        if '..' in codepoint_or_range:
            start, end = codepoint_or_range.split('..')
        else:
            start = end = codepoint_or_range

        # have to use end + 1 because the ranges specified up til here are _inclusive_ ranges.
        for codepoint in range(int(start, base=16), int(end, base=16) + 1):
            result[codepoint].classes.add(codepoint_class)
            if comment:
                result[codepoint].comments.add(comment)
    return result


def _scan_codepoints_file(data_directory: str) -> Iterable[Tuple[str, str, Optional[str]]]:
    """Returns an Iterable of tuples from the codepoints file. Each Tuple is:
    - codepoint / or range of codepoints. Examples: "2139", "2194..2199"
    - unicode class
    - any comment found on that line (useful for debugging.)
    """
    path = os.path.join(data_directory, 'emoji-data.txt')
    with open(path, 'r') as file:
        # NOTE(fabian): I thought about using the csv module for this, but decided against it
        # because of  the fact that the file structure has comments with # at the end. If you _did_
        # want to change this to CSV, I'd probably do it by wrapping `file` with something that
        # stripped comments.
        for line in file:
            line, comment = _remove_comment(line)
            if not line:
                # It was just a comment, continue
                continue

            codepoint_or_range, unicode_class = (field.strip() for field in line.split(';'))
            yield codepoint_or_range, unicode_class, comment


def _remove_comment(line: str) -> Tuple[str, Optional[str]]:
    """Returns: [data-part of line] [comment]"""
    vals = line.split('#', maxsplit=1)
    if len(vals) == 1:
        # There is no comment if there is one element
        return vals[0].strip(), None
    else:
        return vals[0].strip(), vals[1].strip()


def _get_gender_mode(codepoint: _CodePoint) -> GenderMode:
    if codepoint in supplement.SUPPORTS_OBJECT_FORMAT_GENDERING:
        return GenderMode.OBJECT_FORMAT
    elif codepoint in supplement.SUPPORTS_SIGN_FORMAT_GENDERING:
        return GenderMode.SIGN_FORMAT
    else:
        return GenderMode.NONE


def load_emoji_and_modifiers() -> EmojiData:
    """Returns a list of all Emoji and all Modifiers from the data source."""
    emojis: List[Emoji] = []
    modifiers: List[Modifier] = []
    for k, v in _load_codepoints('datasources/emoji-unicode-11/').items():
        if (v.classes & {'Emoji', 'Emoji_Component'}) == {'Emoji'}:
            modifiable = 'Emoji_Modifier_Base' in v.classes
            defaults_to_text = 'Emoji_Presentation' not in v.classes
            gender_mode = _get_gender_mode(k)

            if gender_mode == GenderMode.OBJECT_FORMAT:
                # The non-gendered case has a different meaning from the gendered cases, so add both
                # an Emoji with GenderMode.NONE _and_ an Emoji with GenderMode.OBJECT_FORMAT. The
                # gendered cases are always modifiable (by manually examining the spec).
                emojis.append(Emoji(k, defaults_to_text, modifiable, GenderMode.NONE))
                emojis.append(Emoji(k, defaults_to_text, True, GenderMode.OBJECT_FORMAT))
            else:
                emojis.append(Emoji(k, defaults_to_text, modifiable, gender_mode))
        elif {'Emoji', 'Emoji_Modifier'} <= v.classes:
            # it's a modifier!
            modifiers.append(chr(k))
        else:
            # ??? i dunno something else. It's probably better to handle this exhaustively.
            pass
    return EmojiData(emojis, modifiers)
