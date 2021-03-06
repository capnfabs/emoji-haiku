"""Type stubs for AWS.

Copied from: https://gist.github.com/alexcasalboni/a545b68ee164b165a74a20a5fee9d133

This is an _actual python file_ because there isn't a corresponding python file, so a pyi file
doesn't work. It doesn't cause any problems, because this code is never actually _used_.
"""
from typing import Any, Dict

LambdaDict = Dict[str, Any]


class LambdaCognitoIdentity(object):
    cognito_identity_id: str
    cognito_identity_pool_id: str


class LambdaClientContextMobileClient(object):
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str


class LambdaClientContext(object):
    client: LambdaClientContextMobileClient
    custom: LambdaDict
    env: LambdaDict


class LambdaContext(object):
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: LambdaCognitoIdentity
    client_context: LambdaClientContext

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        ...
