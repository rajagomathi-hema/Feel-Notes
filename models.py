from mongoengine import *
from uuid import uuid4
from datetime import datetime

class User(Document):
    id = StringField(default = lambda: str(uuid4()), primary_key = True)

    name = StringField(required = True )
    email = EmailField(required = True, unique = True)
    password = StringField(required = True)
    phoneNumber = StringField()

    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()

class Note(Document):
    
    id = StringField(default = lambda: str(uuid4()), primary_key = True)

    content = StringField( required = True )
    mood = StringField()
    reaction = StringField()

    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()

    
class CalmZone(Document):
    
    id = StringField(default = lambda: str(uuid4()), primary_key = True)

    content = StringField( required = True )

    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()

class SaveNote(Document):

    id = StringField(default = lambda: str(uuid4()), primary_key = True)

    note = ReferenceField(Note, required = True)
    user = ReferenceField(User, required = True, reverse_delete_rule=CASCADE)

    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()
        
        
