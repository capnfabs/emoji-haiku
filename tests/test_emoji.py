from emoji.core import Gender
from tests.fixture_emoji import baby_angel, detective, genie, index_pointing_up, pencil, \
    police_officer, tent, MODIFIER_SKIN_TONE_DARK


def from_cps(codepoints: str) -> str:
    """The unicode datafiles often contain entries in this format, which is super useful for
    copy-pasting reference test cases.
    """
    return ''.join(chr(int(cp, 16)) for cp in codepoints.split())


def test_renders_emoji_presentation():
    # This Emoji defaults to text, check that it renders as Emoji
    assert pencil.char() == from_cps('270F FE0F')


def test_renders_emoji_presentation_default_emoji():
    # This Emoji defaults to Emoji, check that it doesn't have an extra presentation char
    assert tent.char() == from_cps('26FA')


def test_modifiable_default_emoji_with_no_modifier():
    # This doesn't default to text, so there should be no FE0F afterwards.
    assert baby_angel.char() == from_cps('1F47C')


def test_modifiable_default_emoji_with_modifier():
    assert baby_angel.char(modifier=MODIFIER_SKIN_TONE_DARK) == from_cps('1F47C 1F3FF')


def test_modifiable_default_text_with_modifier():
    """According to spec:
    > Emoji presentation selectors are neither needed nor recommended for emoji characters when
    > they are followed by emoji modifiers, and should not be used in newly generated emoji
    > modifier sequences; the emoji modifier automatically implies the emoji presentation style.
    """

    # Note absence of trailing FE0F
    assert index_pointing_up.char(modifier=MODIFIER_SKIN_TONE_DARK) == from_cps('261D 1F3FF')


def test_modifiable_default_text_no_modifier():
    """Corollary to test_modifiable_default_text_with_modifier."""

    # Note presence of trailing FE0F
    assert index_pointing_up.char() == from_cps('261D FE0F')


def test_gendered_role_emoji_modifiable():
    assert police_officer.char() == from_cps('1F46E')
    assert (police_officer.char(gender=Gender.FEMININE) ==
            from_cps('1F46E 200D 2640 FE0F'))
    assert (
        police_officer.char(
            gender=Gender.FEMININE,
            modifier=MODIFIER_SKIN_TONE_DARK) ==
        from_cps('1F46E 1F3FF 200D 2640 FE0F'))


def test_gendered_role_emoji_nonmodifiable():
    assert genie.char(gender=Gender.MASCULINE) == from_cps('1F9DE 200D 2642 FE0F')


def test_gendered_role_with_modifiers_default_text():
    assert detective.char() == from_cps('1F575 FE0F')
    assert detective.char(gender=Gender.FEMININE) == from_cps('1F575 FE0F 200D 2640 FE0F')
    assert (
        detective.char(
            gender=Gender.FEMININE,
            modifier=MODIFIER_SKIN_TONE_DARK) ==
        from_cps('1F575 1F3FF 200D 2640 FE0F'))
    assert detective.char(modifier=MODIFIER_SKIN_TONE_DARK) == from_cps('1F575 1F3FF')


def test_from_cps():
    """Have to test your utility functions."""
    assert from_cps('270F FE0F') == '\u270F\uFE0F'
