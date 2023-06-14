from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError, validates


class UserSchema(Schema):
    """
    -user schema validation
    -avail id only during serialization
    -exclude passwords on serialization
    -make fields required
    -exclude unknown fields
    """
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True,
                          error_messages={
                              "required": "username is required",
                          },
                          validate=validate.Length(
                              min=2, max=15, error="username must be between 2 and 15 characters")
                          )
    phone_number = fields.Str(required=True,
                              error_messages={
                                  "required": "phone number is required"},
                              validate=validate.Length(
                                  10, error="please enter a valid phone number")
                              )
    password = fields.Str(load_only=True,
                          required=True,
                          error_messages={"required": "password is required"},
                          validate=validate.Length(
                              min=8, max=255, error="password must be between 8 and 30 characters")
                          )

    class Meta:
        unknown = EXCLUDE
