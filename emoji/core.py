"""Renders emojis into unicode sequences."""
import enum
from typing import NamedTuple

from emoji import emoji_unicode_11_manual_supplement as supplement

# Append these to a string to force text / emoji display.
# The Emoji_Presentation unicode property defines the default - if this isn't present, the default
# is (usually) text. The rules are complicated and in The Spec, and encoded in the Emoji class.
_TEXT_PRESENTATION_SELECTOR = '\uFE0E'
_EMOJI_PRESENTATION_SELECTOR = '\uFE0F'

# Zero-width join character.
_ZWJ = '\u200D'

# A string consisting of a single unicode character, which should have the EmojiModifier property
# (which corresponds to a skin color).
Modifier = str


class _GenderMode(enum.Enum):
    # The character doesn't support modification based on gender.
    NONE = enum.auto()
    # The character can be gender-modified, using Sign Format (see The Spec).
    SIGN_FORMAT = enum.auto()
    # The character can be gender-modified, using Object Format (see The Spec).
    OBJECT_FORMAT = enum.auto()


class _GenderRepresentation(NamedTuple):
    sign_format: str
    object_format: str


class Gender(enum.Enum):
    # Don't try and dereference this one :D
    NEUTRAL = None
    MASCULINE = _GenderRepresentation(supplement.MALE, supplement.MAN)
    FEMININE = _GenderRepresentation(supplement.FEMALE, supplement.WOMAN)


class Emoji:
    def __init__(
            self,
            codepoint: int,
            defaults_to_text: bool,
            supports_modification: bool,
            gender_mode: _GenderMode):
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
                # > Emoji presentation selectors are neither needed nor recommended for emoji
                # > characters when they are followed by emoji modifiers, and should not be used in
                # > newly generated emoji modifier sequences; the emoji modifier automatically
                # > implies the emoji presentation style.
                built_str += modifier

        if gender != Gender.NEUTRAL:
            assert self.supports_gender

        if gender != Gender.NEUTRAL and self.gender_mode == _GenderMode.OBJECT_FORMAT:
            built_str += gender.value.object_format
            # The modifier has to go before the join here, which is super inconvenient. Probably
            # the 'correct' way to represent these is with the role as the modifier, and 'man' as
            # the object, but that doesn't work super well for the whole purpose of this code, in
            # that we want to be able to enumerate emoji and then gender/race bend them.
            maybe_add_modifier()
            built_str += _ZWJ

        built_str += self.base_char

        maybe_add_modifier()

        if gender != Gender.NEUTRAL and self.gender_mode == _GenderMode.SIGN_FORMAT:
            built_str += _ZWJ + gender.value.sign_format

        # TODO(fabian): I think there's a bug here where we're rendering the presentation selector
        # when we shouldn't be.
        if self.defaults_to_text:
            # If you want to validate that the sequence constructed here is correct, the datasource
            # for this is in emoji-variation-sequences.txt.
            built_str += _EMOJI_PRESENTATION_SELECTOR

        return built_str

    @property
    def supports_gender(self) -> bool:
        return self.gender_mode != _GenderMode.NONE

    def __repr__(self) -> str:
        return (f'Emoji('
                f'codepoint={hex(self.codepoint)[2:]}, '
                f'defaults_to_text={self.defaults_to_text}, '
                f'supports_modification={self.supports_modification}, '
                f'gender_mode={self.gender_mode})')


def to_unicode_cps(data: str) -> str:
    return ' '.join(hex(ord(c))[2:] for c in data)
