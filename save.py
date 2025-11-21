from flask import request, jsonify, Blueprint, session
from models import SaveNote, Note, User

saveBp = Blueprint('saveBp', __name__)

@saveBp.get('/new')
def newNote():
    try:
        sessionUser = session.get('user')
        if not sessionUser:
            return jsonify({"status": "error", "message": "Unauthorized Access! Please login to save unlimited notes."})

        id = request.args.get("id")
        if not id:
            return jsonify({"status": "error", "message": "Id not found."})
        
        note = Note.objects(id=id).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found."})
        
        user = User.objects(id=sessionUser.get('id')).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found."})
        
        saveNote = SaveNote.objects(note=note, user=user)
        if saveNote:
            saveNote.delete()
            return jsonify({"status": "unsaved", "message": "Note unsaved successfully."})

        SaveNote(
            note = note,
            user = user
        ).save()

        return jsonify({"status": "saved", "message": "Note saved successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    
    
@saveBp.get('/getAll')
def getAllNotes():
    try:
        savenotes = SaveNote.objects()

        savenoteList = []
    
        for savenote in savenotes:
            data = {
                "id":savenote.id,
                "note": {
                    "id":savenote.note.id,
                    "content":savenote.note.content,
                    "mood":savenote.note.mood,
                },
                "addedTime": savenote.addedTime,
                "updatedTime":savenote.updatedTime
            }

            savenoteList.append(data)

        return jsonify({"status": "success", "message": "Notes retrived succeessfully","data":savenoteList} )
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
        
@saveBp.get("/getSingle")
def getSingleNote():
    try:

        id = request.args.get("id")

        savenote = SaveNote.objects(id = id).first()

        if not savenote:
            return jsonify({"status": "error", "message": "Note not found"})
        
        noteData = {
            "id":savenote.id,
            "note":savenote.note,
            "addedTime": savenote.addedTime,
            "updatedTime":savenote.updatedTime
        }

        return jsonify({"status": "success", "message": "Note retrived succeessfully", "data": noteData}) 

    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})


@saveBp.delete("/delete")
def deleteNotes():
    try:
        id = request.args.get("id")

        savenote = SaveNote.objects(id = id).first()

        if not savenote:
            return jsonify({"status": "error", "message": "Saved Note not found"})
        
        savenote.delete()

        return jsonify({"status": "success", "message": "Saved Note found and removed from Saved list."}) 
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})