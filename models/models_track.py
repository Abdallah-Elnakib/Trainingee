from mongoengine import Document, StringField, ListField

class Track(Document):
    track_name = StringField(required=True)
    track_data = ListField()
    meta = {'collection': 'tracks'}
