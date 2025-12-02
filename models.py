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
    reaction = DictField(default={
    "😊": 0,
    "😍": 0,
    "😂": 0,
    "😡": 0,
    "😢": 0
})

    userReactions = DictField(default={})
    #isReactedBySessionUser = BooleanField(default=False)
    #lastReactedEmoji = StringField(default=None)

    addedTime = DateTimeField(default = datetime.now())
    updatedTime = DateTimeField()

    @classmethod
    def get_total_reactions(cls):
        return list(cls.objects.aggregate([
            {
                "$group": {
                    "_id": None,
                    "total😊": {"$sum": "$reaction.😊"},
                    "total😍": {"$sum": "$reaction.😍"},
                    "total😂": {"$sum": "$reaction.😂"},
                    "total😡": {"$sum": "$reaction.😡"},
                    "total😢": {"$sum": "$reaction.😢"}
                }
            }
        ]))[0]
    
    @classmethod
    def get_top_note_for_emoji(cls, emoji):
        field = f"reaction.{emoji}"

        result = list(cls.objects.aggregate([
                { "$addFields": { "emojiCount": f"${field}" } },
                { "$sort": { "emojiCount": -1 } },
                { "$limit": 1 }
            ]))

        return result[0] if result else None

    
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
        
        
