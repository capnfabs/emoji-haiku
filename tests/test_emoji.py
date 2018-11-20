from emoji.core import Emoji, GenderMode

MODIFIER_DARK_SKIN = '\U0001F3FF'


def from_cps(codepoints: str) -> str:
    """The unicode datafiles often contain entries in this format, which is super useful for
    copy-pasting reference test cases.
    """
    return ''.join(chr(int(cp, 16)) for cp in codepoints.split())


def test_renders_emoji_presentation():
    # This Emoji defaults to text, check that it renders as Emoji
    pencil = Emoji(
        0x270F,
        defaults_to_text=True,
        supports_modification=False,
        gender_mode=GenderMode.NONE)
    assert pencil.char() == from_cps('270F FE0F')


def test_renders_emoji_presentation_default_emoji():
    # This Emoji defaults to Emoji, check that it doesn't have an extra presentation char
    tent = Emoji(
        0x26FA,
        defaults_to_text=False,
        supports_modification=False,
        gender_mode=GenderMode.NONE)
    assert tent.char() == from_cps('26FA')


def test_modifiable_with_no_modifier():
    baby_angel = Emoji(
        0x1F47C,
        defaults_to_text=False,
        supports_modification=True,
        gender_mode=GenderMode.NONE)  # Baby Angels apparently don't have genders.
    assert baby_angel.char(modifier=MODIFIER_DARK_SKIN) == from_cps('1F47C 1F3FF')


def test_modifiable_with_no_modifier_default_text():
    # According to spec
    # > Emoji presentation selectors are neither needed nor recommended for emoji characters when
    # > they are followed by emoji modifiers, and should not be used in newly generated emoji
    # > modifier sequences; the emoji modifier automatically implies the emoji presentation style.
    index_pointing_up = Emoji(
        0x261d,
        defaults_to_text=True,
        supports_modification=True,
        gender_mode=GenderMode.NONE)
    # Note absence of trailing FE0F
    assert index_pointing_up.char(modifier=MODIFIER_DARK_SKIN) == from_cps('261D 1F3FF')


def test_from_cps():
    """Have to test your utility functions."""
    assert from_cps('270F FE0F') == '\u270F\uFE0F'
