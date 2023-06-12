from marshmallow import Schema, fields, validate, EXCLUDE


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
                          error_messages={"required": "username is required"},
                          validate=validate.Range(min=1, max=15)
                          )
    phone_number = fields.Integer(required=True,
                                  error_messages={
                                      "required": "phone number is required"},
                                  validate=validate.Equal(10)
                                  )
    password = fields.Str(load_only=True,
                          required=True,
                          error_messages={"required": "password is required"},
                          validate=validate.Range(min=8, max=30)
                          )

    class Meta:
        unknown = EXCLUDE
