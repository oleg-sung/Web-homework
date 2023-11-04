import json

from aiohttp import web
from pydantic import ValidationError


def get_http_errors(http_error_class, message):
    return http_error_class(
        text=json.dumps({'errors': message}),
        content_type='application/json')


def validate(json_data, schema):
    try:
        model = schema(**json_data)
        return model.dict(exclude_none=True)
    except ValidationError as err:
        error_message = json.loads(err.json())
        raise get_http_errors(web.HTTPBadRequest, error_message)
