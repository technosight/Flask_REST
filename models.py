from datetime import datetime
from config import db, ma
from marshmallow import fields


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)

    emails = db.relationship(
        'Email',
        backref='user',
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Email.address)")
        # lazy=False)


class Email(db.Model):

    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class UserSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqla_session = db.session

    emails = fields.Nested('UserEmailSchema', default=[], many=True)


class UserEmailSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    id = fields.Int()
    user_id = fields.Int()
    address = fields.Email()
    created_on = fields.DateTime()


class EmailSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    class Meta:
        model = Email
        sqla_session = db.session

    contact = fields.Nested('EmailUserSchema', default=None)


class EmailUserSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    surname = fields.Str()