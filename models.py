from datetime import datetime
from config import db, ma
from marshmallow import fields


class User(db.Model):

    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    surname = db.Column(db.String(50), unique=False, nullable=False)

    contact_details = db.relationship(
        'ContactDetail',
        backref='user',
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(ContactDetail.email)")
        # lazy=False)


class ContactDetail(db.Model):

    __tablename__ = 'contact_detail'

    contact_detail_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    email = db.Column(db.String(100), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class UserSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    class Meta:
        model = User
        sqla_session = db.session

    contact_details = fields.Nested('UserContactDetailSchema', default=[], many=True)


class UserContactDetailSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    contact_detail_id = fields.Int()
    user_id = fields.Int()
    # email = fields.Email()
    email = fields.String()
    created_on = fields.DateTime()


class ContactDetailSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    class Meta:
        model = ContactDetail
        sqla_session = db.session

    user = fields.Nested('ContactDetailUserSchema', default=None)


class ContactDetailUserSchema(ma.ModelSchema):

    def __init__(self, **kwargs):
        # super().__init__(strict=True, **kwargs)
        super().__init__(**kwargs)

    user_id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    surname = fields.Str()