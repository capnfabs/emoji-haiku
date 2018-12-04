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
