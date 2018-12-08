from api import entry


def test_api():
    obj = entry.haiku_handler(None, None)
    # Should be 3 lines of text
    assert obj['emoji'].count('\n') == 2
    assert obj['descriptions'].count('\n') == 2
