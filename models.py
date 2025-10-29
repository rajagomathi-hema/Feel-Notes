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