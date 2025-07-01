from mongoengine import Document, StringField, DateTimeField
import datetime

class Otp(Document):
    email = StringField(required=True)
    otp = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'otp', 'indexes': [{'fields': ['created_at'], 'expireAfterSeconds': 60}]}
