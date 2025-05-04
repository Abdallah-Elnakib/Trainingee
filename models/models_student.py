from mongoengine import Document, StringField, IntField

class Student(Document):
    student_id = IntField(required=True)
    name = StringField(required=True)
    degrees = IntField(required=True)
    additional = IntField(required=True)
    basic_total = IntField(required=True)
    total_degrees = IntField(required=True)
    comments = StringField(required=True)
    meta = {'collection': 'students'}
