"""Super lightweight emoji library."""

from typing import NamedTuple, Tuple, Dict, Set, Iterable, Optional, List
import os.path
from collections import defaultdict
import random
import emoji_unicode_11_manual_supplement as supplement
import enum

CodePoint = int
UnicodeClass = str

# Append these to a string to force text / emoji display.
TEXT_PRESENTATION_SELECTOR = '\uFE0E'
EMOJI_PRESENTATION_SELECTOR = '\uFE0F'
ZWJ = '\u200D'

class CodePointInfo(NamedTuple):
    classes: Set[UnicodeClass]
    comments: Set[str]

Modifier = str

def makeCPI() -> CodePointInfo:
    return CodePointInfo(set(), set())


class GenderMode(enum.Enum):
    NONE = enum.auto()
    SIGN_FORMAT = enum.auto()
    OBJECT_FORMAT = enum.auto()

class GenderRepresentation(NamedTuple):
    sign_format: str
    object_format: str

class Gender(enum.Enum):
    # Don't try and dereference this one :D
    NEUTRAL   = None
    MASCULINE = GenderRepresentation(supplement.MALE, supplement.MAN)
    FEMININE  = GenderRepresentation(supplement.FEMALE, supplement.WOMAN)


class Emoji:
    def __init__(self, codepoint: int, defaults_to_text: bool, supports_modification: bool, gender_mode: GenderMode):
        self.codepoint = codepoint
        self.base_char = chr(codepoint)

        self.defaults_to_text = defaults_to_text
        # Modification actually means 'skin color'. It's a technical term in the spec, though, so
        # we stick with it here.
        self.supports_modification = supports_modification

        self.gender_mode = gender_mode


    def char(self, modifier: Modifier = None, gender: Gender = Gender.NEUTRAL) -> str:
        """Turns the Emoji into a fragment of a string.
        Accepts an optional modifier - if set, the skin color of the emoji will
        be modified. Check supports_modification first.
        """
        # TODO / enhancements:
        # - explicit left/right facing?
        # - ZWJ sequences.

        built_str = ''

        modifier_added = False

        def maybe_add_modifier() -> None:
            # This feels... nasty.
            nonlocal modifier_added
            nonlocal built_str
            nonlocal modifier

            if modifier and not modifier_added:
                assert self.supports_modification
                modifier_added = True
                # As per spec:
                # > Emoji presentation selectors are neither needed nor recommended for emoji characters
                # > when they are followed by emoji modifiers, and should not be used in newly generated
                # > emoji modifier sequences; the emoji modifier automatically implies the emoji
                # > presentation style.
                built_str += modifier

        if gender != Gender.NEUTRAL:
            assert self.gender_mode != GenderMode.NONE

        if gender != Gender.NEUTRAL and self.gender_mode == GenderMode.OBJECT_FORMAT:
            built_str += gender.value.object_format
            # The modifier has to go before the join here, which is super inconvenient. Probably
            # the 'correct' way to represent these is with the role as the modifier, and 'man' as
            # the object, but that doesn't work super well for the whole purpose of this code, in
            # that we want to be able to enumerate emoji and then gender/race bend them.
            maybe_add_modifier()
            built_str += ZWJ

        built_str += self.base_char

        maybe_add_modifier()

        if gender != Gender.NEUTRAL and self.gender_mode == GenderMode.SIGN_FORMAT:
            built_str += ZWJ + gender.value.sign_format

        if self.defaults_to_text:
            # If you want to validate that the sequence constructed here is correct, the datasource
            # for this is in emoji-variation-sequences.txt.
            built_str += EMOJI_PRESENTATION_SELECTOR

        return built_str

    def __repr__(self) -> str:
        return f'Emoji(codepoint={hex(self.codepoint)[2:]}, defaults_to_text={self.defaults_to_text}, supports_modification={self.supports_modification}, gender_mode={self.gender_mode})'


def load_codepoints(data_directory: str) -> Dict[CodePoint, CodePointInfo]:
    """Returns a Dict mapping every possible emoji character to information known about it, from the
    unicode data specification.
    """
    result: Dict[CodePoint, CodePointInfo] = defaultdict(makeCPI)
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


def _scan_codepoints_file(data_directory: str) -> Iterable[Tuple[str,str, Optional[str]]]:
    """Returns an Iterable of tuples from the codepoints file. Each Tuple is:
    - codepoint (or range of codepoints)
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

            fields = [field.strip() for field in line.split(';')]
            assert len(fields) == 2
            # Codepoint or range, class
            yield fields[0], fields[1], comment


def _remove_comment(line: str) -> Tuple[str, Optional[str]]:
    """Returns: [data-part of line] [comment]"""
    vals = line.split('#', maxsplit=1)
    if len(vals) == 1:
        # There is no comment if there is one element
        return vals[0].strip(), None
    else:
        return vals[0].strip(), vals[1].strip()


class EmojiData(NamedTuple):
    emojis: List[Emoji]
    modifiers: List[Modifier]


def _get_gender_mode(codepoint: int) -> GenderMode:
    if codepoint in supplement.SUPPORTS_OBJECT_FORMAT_GENDERING:
        return GenderMode.OBJECT_FORMAT
    elif codepoint in supplement.SUPPORTS_SIGN_FORMAT_GENDERING:
        return GenderMode.SIGN_FORMAT
    else:
        return GenderMode.NONE


def make_data() -> EmojiData:
    emojis: List[Emoji] = []
    modifiers: List[Modifier] = []
    for k, v in load_codepoints('datasources/emoji-unicode-11/').items():
        if (v.classes & {'Emoji', 'Emoji_Component'}) == {'Emoji'}:
            modifiable = 'Emoji_Modifier_Base' in v.classes
            defaults_to_text = 'Emoji_Presentation' not in v.classes
            gender_mode = _get_gender_mode(k)
            emojis.append(Emoji(k, defaults_to_text, modifiable, gender_mode))
        elif (v.classes & {'Emoji', 'Emoji_Modifier'}) == {'Emoji', 'Emoji_Modifier'}:
            # it's a modifier!
            modifiers.append(chr(k))
        else:
            # ??? i dunno something else.
            pass
    return EmojiData(emojis, modifiers)

def yield_swatch_chars(emoji: List[Emoji], mods: List[Modifier]) -> Iterable[str]:
    """Debug method: takes a list of emoji and possible modifiers and yields each one in turn.
    Anything modifiable gets a random modification.

    You can use the output as an argument to `str.join` and then print it.
    """
    emoji, mods = make_data()

    for e in emoji:
        modifier = random.choice(mods) if e.supports_modification else None
        gender = random.choice(list(Gender)) if e.gender_mode != GenderMode.NONE else Gender.NEUTRAL
        char = e.char(modifier=modifier, gender=gender)
        yield char + ' --> ' + to_unicode_cps(char)


def to_unicode_cps(data: str) -> str:
    return ' '.join(hex(ord(c))[2:] for c in data)


def main() -> None:
    emoji, mods = make_data()
    print('\n'.join(yield_swatch_chars(emoji, mods)))


if __name__ == "__main__":
    main()
