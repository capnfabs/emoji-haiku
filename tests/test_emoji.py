from emoji.core import Emoji, Gender, GenderMode

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


baby_angel = Emoji(
        0x1F47C,
        defaults_to_text=False,
        supports_modification=True,
        gender_mode=GenderMode.NONE)  # Baby Angels apparently don't have genders.


def test_modifiable_default_emoji_with_no_modifier():
    # This doesn't default to text, so there should be no FE0F afterwards.
    assert baby_angel.char() == from_cps('1F47C')


def test_modifiable_default_emoji_with_modifier():
    assert baby_angel.char(modifier=MODIFIER_DARK_SKIN) == from_cps('1F47C 1F3FF')


# We could probably use a fixture for this, but we don't need it.
# I don't understand what benefit a fixture would provide in this scenario, but maybe I should
# make an effort to understand that sometime.
index_pointing_up = Emoji(
        0x261d,
        defaults_to_text=True,
        supports_modification=True,
        gender_mode=GenderMode.NONE)


def test_modifiable_default_text_with_modifier():
    """According to spec:
    > Emoji presentation selectors are neither needed nor recommended for emoji characters when
    > they are followed by emoji modifiers, and should not be used in newly generated emoji
    > modifier sequences; the emoji modifier automatically implies the emoji presentation style.
    """

    # Note absence of trailing FE0F
    assert index_pointing_up.char(modifier=MODIFIER_DARK_SKIN) == from_cps('261D 1F3FF')


def test_modifiable_default_text_no_modifier():
    """Corollary to test_modifiable_default_text_with_modifier."""

    # Note presence of trailing FE0F
    assert index_pointing_up.char() == from_cps('261D FE0F')


police_officer = Emoji(
    0x1F46E,
    defaults_to_text=False,
    supports_modification=True,
    gender_mode=GenderMode.SIGN_FORMAT)


def test_gendered_role_emoji_modifiable():
    assert police_officer.char() == from_cps('1F46E')
    assert (police_officer.char(gender=Gender.FEMININE) ==
            from_cps('1F46E 200D 2640 FE0F'))
    assert (
        police_officer.char(
            gender=Gender.FEMININE,
            modifier=MODIFIER_DARK_SKIN) ==
        from_cps('1F46E 1F3FF 200D 2640 FE0F'))


genie = Emoji(
    0x1F9DE,
    defaults_to_text=False,
    supports_modification=False,
    gender_mode=GenderMode.SIGN_FORMAT)


def test_gendered_role_emoji_nonmodifiable():
    assert genie.char(gender=Gender.MASCULINE) == from_cps('1F9DE 200D 2642 FE0F')


detective = Emoji(
    0x1F575,
    defaults_to_text=True,
    supports_modification=True,
    gender_mode=GenderMode.SIGN_FORMAT)


def test_gendered_role_with_modifiers_default_text():
    assert detective.char() == from_cps('1F575 FE0F')
    assert detective.char(gender=Gender.FEMININE) == from_cps('1F575 FE0F 200D 2640 FE0F')
    assert (
        detective.char(
            gender=Gender.FEMININE,
            modifier=MODIFIER_DARK_SKIN) ==
        from_cps('1F575 1F3FF 200D 2640 FE0F'))
    assert detective.char(modifier=MODIFIER_DARK_SKIN) == from_cps('1F575 1F3FF')


def test_from_cps():
    """Have to test your utility functions."""
    assert from_cps('270F FE0F') == '\u270F\uFE0F'
