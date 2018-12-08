"""Renders emojis into unicode sequences."""
import enum
from typing import NamedTuple, Any, Tuple

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


class GenderMode(enum.Enum):
    # The character doesn't support modification based on gender.
    NONE = enum.auto()
    # The character can be gender-modified, using Sign Format (see The Spec).
    SIGN_FORMAT = enum.auto()
    # The character _must_ be gender-modified, using Object Format (see The Spec), in order to
    # retain its fundamental meaning. An example:
    #  - 1F468 200D 1F3EB is 'man teacher'
    #  - 1F469 200D 1F3EB is 'woman teacher'
    #  - 1F3EB is 'school'.
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
            gender_mode: GenderMode):
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

        This is a mess:
        http://www.unicode.org/reports/tr51/tr51-14.html#Emoji_Variation_Selector_Notes
        """
        # TODO / enhancements:
        # - explicit left/right facing?

        built_str = ''

        if gender != Gender.NEUTRAL:
            assert self.supports_gender

        if self.must_gender:
            # Force users to explicitly choose, rather than choose a default. Alternatively, I'd be
            # sorta happy to just pick one randomly, but the non-determinism of that is scary for
            # something that's supposed to be relatively well encapsulated.
            assert gender != Gender.NEUTRAL

        if self.gender_mode == GenderMode.OBJECT_FORMAT:
            # This is an entirely different way of building an emoji. This is because this mode has
            # the MAN or WOMAN emoji as the primary emoji, and then the action is a secondary which
            # is joined on to the end. It would probably be cleaner to abstract this somehow to
            # follow that paradigm, but this is a pretty niche case, so let's just test the crap out
            # of it instead.
            built_str += gender.value.object_format
            if modifier:
                built_str += modifier
            # Note that neither the MAN nor the WOMAN character have default text presentation, so
            # we never need to add the EMOJI_PRESENTATION_SELECTOR here.

            built_str += _ZWJ
            built_str += self.base_char
            if self.defaults_to_text:
                built_str += _EMOJI_PRESENTATION_SELECTOR
            return built_str

        built_str += self.base_char

        if modifier:
            # Modifiers imply _EMOJI_PRESENTATION_SELECTOR, so it's never required.
            built_str += modifier
        elif self.defaults_to_text:
            built_str += _EMOJI_PRESENTATION_SELECTOR

        if gender != Gender.NEUTRAL and self.gender_mode == GenderMode.SIGN_FORMAT:
            # The sign_format chars require presentation selectors.
            built_str += _ZWJ + gender.value.sign_format + _EMOJI_PRESENTATION_SELECTOR

        return built_str

    def _tuple(self) -> Tuple:
        """Returns a tuple representation of the object, which includes _all information_ which
        makes up the object definition. Use this for equality comparisons and hashing, for example.
        """
        return self.codepoint, self.defaults_to_text, self.supports_modification, self.gender_mode

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Emoji):
            return False
        return self._tuple() == other._tuple()

    def __hash__(self) -> int:
        return self._tuple().__hash__()

    @property
    def supports_gender(self) -> bool:
        return self.gender_mode != GenderMode.NONE

    @property
    def must_gender(self) -> bool:
        """Certain emoji _must_ be gendered to retain meaning, or otherwise they have a different
        visual appearance. For example:
        ⚕ = "medical symbol", 👨‍⚕= "man health worker", 👩‍⚕= "woman health worker".
        """
        return self.gender_mode == GenderMode.OBJECT_FORMAT

    def __repr__(self) -> str:
        return (f'Emoji('
                f'codepoint={hex(self.codepoint)[2:]}, '
                f'defaults_to_text={self.defaults_to_text}, '
                f'supports_modification={self.supports_modification}, '
                f'gender_mode={self.gender_mode})')


def to_unicode_cps(data: str) -> str:
    return ' '.join(hex(ord(c))[2:] for c in data)
