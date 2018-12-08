"""Tests to make sure that scripts don't get randomly broken."""


def test_swatch():
    from scripts import swatch
    swatch.main()
