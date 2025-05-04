from mongoengine import connect, Document, StringField
import os
connect('test', host='mongodb://localhost:27017/')

class User(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    role = StringField(required=True)
    reset_password_token = StringField()
    meta = {'collection': 'users'}




