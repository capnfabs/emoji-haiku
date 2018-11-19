# The emoji-zwj-sequences.txt file is hard to parse in an automated fashion for the stuff I want to
# do, so we're doing it by hand.
#
# Everything in 'Emoji ZWJ Sequence: Gendered Role, with object' supports gendering and skin color.
# format: man_or_woman this_code
GENDERED_ROLE_WITH_OBJECT__OBJECTS = {
    0x2695,
    0x2696,
    0x2708,
    0x1F33E,
    0x1F373,
    0x1F393,
    0x1F3A4,
    0x1F3A8,
    0x1F3EB,
    0x1F3ED,
    0x1F4BB,
    0x1F4BC,
    0x1F527,
    0x1F52C,
    0x1F680,
    0x1F692,
    0x1F9B0,
    0x1F9B1,
    0x1F9B2,
    0x1F9B3,
}


# Have to use 32-bit representation for this because it's a high-end codepoint.
MAN = '\U0001F468'
WOMAN = '\U0001F469'


# This is the 'Emoji ZWJ Sequence: Gendered Role' section.
# Format: this_code skin_color ZWJ gender emoji_presentation
GENDERED_ROLE__OBJECTS = {
    0x1F46E,
    0x1F471,
    0x1F473,
    0x1F477,
    0x1F482,
    0x1F575,
    0x1F9D9,
    0x1F9DA,
    0x1F9DB,
    0x1F9DC,
    0x1F9DD,
    0x1F9DE,
    0x1F9DF,
}


FEMALE = '\u2640'
MALE = '\u2642'


# Emoji ZWJ Sequence: Gendered Activity
# Format: this_code skin_color ZWJ gender emoji_presentation
GENDERED_ACTIVITY__OBJECTS = {
    0x1F3C3,
    0x1F3C4,
    0x1F3CA,
    0x1F3CB,
    0x1F3CC,
    0x1F46F,
    0x1F486,
    0x1F487,
    0x1F6A3,
    0x1F6B4,
    0x1F6B5,
    0x1F6B6,
    0x1F938,
    0x1F939,
    0x1F93C,
    0x1F93D,
    0x1F93E,
    0x1F9D6,
    0x1F9D7,
    0x1F9D8,
    0x26F9,
}


# Emoji ZWJ Sequence: Gendered Gestures
GENDERED_GESTURES__OBJECTS = {
    0x1F481,
    0x1F645,
    0x1F646,
    0x1F647,
    0x1F64B,
    0x1F64D,
    0x1F64E,
    0x1F926,
    0x1F937,
    0x1F9B8,
    0x1F9B9,
}


SUPPORTS_SIGN_FORMAT_GENDERING = (
    GENDERED_ACTIVITY__OBJECTS |
    GENDERED_GESTURES__OBJECTS |
    GENDERED_ROLE__OBJECTS)
SUPPORTS_OBJECT_FORMAT_GENDERING = GENDERED_ROLE_WITH_OBJECT__OBJECTS


# TODO:
# Emoji ZWJ Sequence: Other
# Emoji ZWJ Sequence: Family
# Flags?
