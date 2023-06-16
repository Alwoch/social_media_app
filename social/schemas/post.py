from marshmallow import Schema, fields, validate, EXCLUDE
from .user import UserSchema


class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, error_messages={
                       "required": "post must have a title"}, validate=validate.Length(max=255, error='title is too long'))
    content = fields.Str(required=True, error_messages={
                         "required": "post must have body"})
    created_at = fields.DateTime(dump_only=True)
    author = fields.Nested(UserSchema, only=("id", "username"), dump_only=True)
