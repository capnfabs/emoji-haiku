from typing import Any

from api.aws import LambdaContext

from haiku import haiku


def haiku_handler(_: Any, __: LambdaContext) -> Any:
    """AWS Lambda entrypoint. Generates a single Haiku."""
    h = haiku()
    return {
        'emoji': h[0],
        'descriptions': h[1],
    }
