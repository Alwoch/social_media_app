from social import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text as sa_text

from .base import Base


class User(db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   server_default=sa_text("uuid_generate_v4()"))
    username = db.Column(db.String(15), unique=True, nullable=False)
    phone_number = db.Column(db.Integer(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __init__(self, username, phone_number, password):
        self.username = username
        self.phone_number = phone_number
        self.password = password
