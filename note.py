from flask import request, jsonify, Blueprint, session
from models import *

noteBp = Blueprint('noteBp', __name__)

@noteBp.post('/new')
def newNote():
    try:
        data = request.get_json()

        content = data.get('content')
        mood = data.get('mood')
        # reaction = data.get('reaction')
        
        if not content or not mood:
            return jsonify({"status": "error", "message": "All fields required."})
            
        Note(
            content = content,
            mood = mood,
            # reaction = reaction,
        ).save()

        return jsonify({"status": "success", "message": "Note created Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    
    
@noteBp.put("/update")
def updateNote():
    try:
        id = request.args.get("id")
        data = request.get_json()

        content = data.get('content')
        mood = data.get('mood')
        reaction = data.get('reaction')
        
        note = Note.objects(id=id).first()
        
        if not note:
            return jsonify({"status": "error", "message": "Note not found"})
        
        note.content = content
        note.mood = mood
        note.reaction = reaction
        
        return jsonify({"status": "success", "message": "Note Updated Successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    
    
@noteBp.get('/getAll')
def getAllNotes():
    try:
        sessionUser = session.get('user')
        if not sessionUser:
            return jsonify({"status": "error", "message": "Unauthorized Access! Please login to see more notes."})

        user = User.objects(id=sessionUser.get('id')).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found."})

        notes = Note.objects()

        noteList = []
    
        for note in notes:
            isSaved = False
            saveNote = SaveNote.objects(note=note, user=user)
            if saveNote:
                isSaved = True

            data = {
                "id":note.id,
                "content":note.content,
                "mood":note.mood,
                "reaction":note.reaction,
                "addedTime": note.addedTime,
                "updatedTime":note.updatedTime,
                'isSaved': isSaved
            }

            noteList.append(data)

        return jsonify({"status": "success", "message": "Notes retrived succeessfully","data":noteList} )
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
        
@noteBp.get("/getSingle")
def getSingleNote():
    try:

        id = request.args.get("id")

        note = Note.objects(id = id).first()

        if not note:
            return jsonify({"status": "error", "message": "Note not found"})
        
        noteData = {
            "id":note.id,
            "content":note.content,
            "mood":note.mood,
            "reaction":note.reaction,
            "addedTime": note.addedTime,
            "updatedTime":note.updatedTime
        }

        return jsonify({"status": "success", "message": "Note retrived succeessfully", "data": noteData}) 

    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})


@noteBp.delete("/delete")
def deleteNotes():
    try:
        id = request.args.get("id")

        note = Note.objects(id = id).first()

        if not note:
            return jsonify({"status": "error", "message": "Note not found"})
        
        note.delete()

        return jsonify({"status": "success", "message": "Note found and removed from notes list."}) 
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})