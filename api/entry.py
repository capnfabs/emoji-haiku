import json
from typing import Any

from api.aws import LambdaContext

import haiku

gender_mapping = {
    'm': haiku.RenderGender.MASCULINE,
    'f': haiku.RenderGender.FEMININE,
}


def _http400(message: str) -> Any:
    return {
        "isBase64Encoded": False,
        "statusCode": 400,
        "headers": {
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps(message)
    }


def haiku_handler(event: Any, context: LambdaContext) -> Any:
    """AWS Lambda entrypoint. Generates a single Haiku."""
    # Have to use `get() or {}` because the key is sometimes present, but None.
    query = event.get('queryStringParameters') or {}
    gender_str = query.get('gender', '').lower()
    if gender_str and gender_str not in gender_mapping:
        return _http400(f"Expected gender of 'm', 'f' or unset, got '{gender_str}' ")
    gender = gender_mapping.get(gender_str, haiku.RenderGender.DONT_CARE)
    modifier = query.get('modifier')
    if modifier and modifier not in haiku.modifiers:
        return _http400(f'Got unknown modifier: {modifier}')
    h = haiku.formatted_haiku(gender, modifier)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
        },
        "body": json.dumps({
            'emoji': h[0],
            'descriptions': h[1],
        })
    }
