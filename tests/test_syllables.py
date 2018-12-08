import pytest

import syllables


def test_syllable_count():
    # Cam-ra or Cam-e-ra
    assert syllables.count_syllables("camera") == {2, 3}
    # You'd be pretty crazy to pronounce this as Cam-ra, Cam-er-a but we'll allow it.
    assert syllables.count_syllables("camera, camera") == {4, 5, 6}
    assert syllables.count_syllables("Unicorn?!") == {3}
    assert syllables.count_syllables("Yes, Unicorn.") == {4}
    assert syllables.count_syllables("truffles") == {2}
    assert syllables.count_syllables("No, *you're* crazy!") == {4}

    # TODO(fabian): right now this doesn't work, because we're not smart enough to consider this as
    #   two separate words. We want to fix that if we're ever accepting "general" input, instead of
    #   just input from the unicode spec.

    # assert syllables.count_syllables("Unfathomable!Potatos") == {8}


def test_overrides():
    # Stuff that's not in the cmudict database
    assert syllables.count_syllables('1st') == {1}
    assert syllables.count_syllables('sauropod') == {3}

    # Stuff that's in the database, but which is also wrong
    # In emoji this is only Sa-ke 🍶
    assert syllables.count_syllables('sake') == {2}


def test_throws_when_cant_find_word():
    assert syllables.count_syllables("rex") == {1}
    with pytest.raises(KeyError):
        syllables.count_syllables("gronkasaurus rex")
