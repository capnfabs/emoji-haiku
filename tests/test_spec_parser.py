from emoji import spec_parser
from tests.fixture_emoji import ALL_FIXTURE_EMOJI, ALL_KNOWN_MODIFIERS


def test_sample_emojis():
    """
    Testing strategy - I didn't want to bother with Dependency Injection for this (and writing my
    own fake emoji-unicode-11 directory) so instead, we're just verifying that the outputs match
    some pre-verified emoji that I've checked manually.
    """
    emoji, modifiers = spec_parser.load_emoji_and_modifiers()
    for expected_emoji in ALL_FIXTURE_EMOJI:
        assert expected_emoji in emoji

    assert set(modifiers) == set(ALL_KNOWN_MODIFIERS)
