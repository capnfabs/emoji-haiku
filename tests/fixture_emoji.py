"""
Some sample emoji objects from the spec that I've manually verified.

We could probably use pytest fixtures for these, but we don't need that right now. I don't
understand what benefit a fixture would provide in this scenario, but maybe I should make an effort
to understand that sometime.
"""

from emoji.core import Emoji, GenderMode

pencil = Emoji(
    0x270F,
    defaults_to_text=True,
    supports_modification=False,
    gender_mode=GenderMode.NONE)


tent = Emoji(
    0x26FA,
    defaults_to_text=False,
    supports_modification=False,
    gender_mode=GenderMode.NONE)


baby_angel = Emoji(
    0x1F47C,
    defaults_to_text=False,
    supports_modification=True,
    gender_mode=GenderMode.NONE)  # Baby Angels apparently don't have genders.


index_pointing_up = Emoji(
    0x261d,
    defaults_to_text=True,
    supports_modification=True,
    gender_mode=GenderMode.NONE)


police_officer = Emoji(
    0x1F46E,
    defaults_to_text=False,
    supports_modification=True,
    gender_mode=GenderMode.SIGN_FORMAT)


detective = Emoji(
    0x1F575,
    defaults_to_text=True,
    supports_modification=True,
    gender_mode=GenderMode.SIGN_FORMAT)


genie = Emoji(
    0x1F9DE,
    defaults_to_text=False,
    supports_modification=False,
    gender_mode=GenderMode.SIGN_FORMAT)


# I've historically had a lot of trouble getting object-format gendered emojis correct. 'Judge' and
# 'Balance scale' are two separate visual emoji. 'Judge' is comprised of MAN or WOMAN + ZWJ +
# BALANCE SCALE, so I added both of these to the test to ensure that they're correctly and
# separately interpreted.
judge = Emoji(
    0x2696,
    defaults_to_text=True,
    supports_modification=True,
    gender_mode=GenderMode.OBJECT_FORMAT
)

balance_scale = Emoji(
    0x2696,
    defaults_to_text=True,
    supports_modification=False,
    gender_mode=GenderMode.NONE,
)


MODIFIER_SKIN_TONE_LIGHT = '\U0001F3FB'
MODIFIER_SKIN_TONE_MEDIUM_LIGHT = '\U0001F3FC'
MODIFIER_SKIN_TONE_MEDIUM = '\U0001F3FD'
MODIFIER_SKIN_TONE_MEDIUM_DARK = '\U0001F3FE'
MODIFIER_SKIN_TONE_DARK = '\U0001F3FF'


ALL_FIXTURE_EMOJI = [
    pencil,
    tent,
    baby_angel,
    index_pointing_up,
    police_officer,
    detective,
    genie,
    judge,
    balance_scale,
]


ALL_KNOWN_MODIFIERS = [
    MODIFIER_SKIN_TONE_LIGHT,
    MODIFIER_SKIN_TONE_MEDIUM_LIGHT,
    MODIFIER_SKIN_TONE_MEDIUM,
    MODIFIER_SKIN_TONE_MEDIUM_DARK,
    MODIFIER_SKIN_TONE_DARK,
]
