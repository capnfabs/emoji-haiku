from haiku import Haiku, RenderGender
from tests.fixture_emoji import police_officer
from parameterized import parameterized


@parameterized.expand([
    (RenderGender.DONT_CARE, None, 5, 2),
    (RenderGender.FEMININE, None, 5, 1),
    (RenderGender.DONT_CARE, '🏿', 1, 2),
    (RenderGender.FEMININE, '🏿', 1, 1),
])
def test_formatter(gender, modifier, expected_num_skin_colors, expected_num_genders):
    """It's pretty hard to test that emojis are generated correctly, but it's easy to test that the
    formatting works, especially when you choose to force skin color or gender. So we do that here,
    probabilistically.
    """

    # This is violating a bunch of the expectations of the Haiku class, but we can fix that if it's
    # a problem later.
    haiku = Haiku([[police_officer] * 5000], [[]])

    emoji, desc = haiku.format(gender, modifier)
    characters = emoji.split()
    # There should be lots of different variants produced.
    assert len(set(characters)) == expected_num_genders * expected_num_skin_colors
    firsts, seconds = zip(*(c.split('\u200d') for c in characters))
    # First part should have the skin color modifiers, so there should be 5 variants.
    # Probability that there isn't all 5 options out of 1000 tries is pretty low, but I don't want
    # to put in the effort to quantify it.
    assert len(set(firsts)) == expected_num_skin_colors
    # police_officer uses the SIGN gender mode, so splitting on the ZWJ character will give just the
    # gender options. Should be two.
    assert len(set(seconds)) == expected_num_genders
