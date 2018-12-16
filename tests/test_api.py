import json

from api import entry


def test_api():
    obj = entry.haiku_handler({}, None)
    # Should be 3 lines of text
    body = json.loads(obj['body'])
    assert body['emoji'].count('\n') == 2
    assert body['descriptions'].count('\n') == 2
    assert obj['statusCode'] == 200
    assert 'Access-Control-Allow-Origin' in obj['headers']
