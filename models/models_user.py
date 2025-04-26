from mongoengine import Document, StringField

class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    reset_password_token = StringField()
    meta = {'collection': 'users'}




