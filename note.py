from flask import request, jsonify, Blueprint, session
from models import *

noteBp = Blueprint('noteBp', __name__)

@noteBp.post('/new')
def newNote():
    try:
        data = request.get_json()

        content = data.get('content')
        mood = data.get('mood')
        reaction = data.get('reaction')
        
        if not content or not mood:
            return jsonify({"status": "error", "message": "All fields required."})
            
        Note(
            content = content,
            mood = mood,
            reaction = reaction,
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
    
@noteBp.post('/react')
def react():
    try:
        sessionUser = session.get('user')
        if not sessionUser:
            return jsonify({"status": "error", "message": "Unauthorized Access! Please login to see more notes."})

        user = User.objects(id=sessionUser.get('id')).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found."})
        
        user_id = str(user.id)

        data = request.get_json()

        id = data.get('id')
        key = data.get('key')

        if not id or not key:
            return jsonify({"status": "error", "message": "Id, Key or Value is missing."})

        note = Note.objects(id = id).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found"})

        prev = note.userReactions.get(user_id)
        
        # CASE A: User already reacted before
        if prev:

            # A1: User clicked the SAME emoji → remove reaction
            if prev == key:
                note.reaction[key] -= 1
                del note.userReactions[user_id]

            # A2: User clicked DIFFERENT emoji → change reaction
            else:
                note.reaction[prev] -= 1
                note.reaction[key] += 1
                note.userReactions[user_id] = key

        # CASE B: First time reacting
        else:
            note.reaction[key] += 1
            note.userReactions[user_id] = key
        
        note.save()

        return jsonify({"status": "success", "message": "Note Reacted.", 'reactions': note.reaction, 'id': str(note.id)}) 
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    

@noteBp.get('/analytics')
def analytics():
    try:

        # stats = Note.get_total_reactions()
        
        # top_laugh_note = Note.get_top_note_for_emoji("😍")

        # print("Note ID:", top_laugh_note["_id"])
        # print("Content:", top_laugh_note["content"])
        # print("😂 Count:", top_laugh_note["emojiCount"])


        # return stats, top_laugh_note

        # Step 1: Get total reaction counts
        stats = Note.get_total_reactions()

        # stats = { "total😊": 10, "total😍": 25, "total😂": 5, ... }

        # Step 2: Convert stats into a normal dict with emoji → count
        reaction_totals = {
            "😊": stats.get("total😊", 0),
            "😍": stats.get("total😍", 0),
            "😂": stats.get("total😂", 0),
            "😡": stats.get("total😡", 0),
            "😢": stats.get("total😢", 0),
        }

        # Step 3: find the emoji with highest count
        highest_emoji = max(reaction_totals, key=reaction_totals.get)
        highest_count = reaction_totals[highest_emoji]

        print("Highest Reaction:", highest_emoji, "=", highest_count)

        # Step 4: get the note with highest count for that reaction
        top_note = Note.get_top_note_for_emoji(highest_emoji)

        # Step 5: return analytics
        return jsonify({
            "status": "success",
            "highestReaction": highest_emoji,
            "highestReactionCount": highest_count,
            "topNote": top_note,
            "reactionTotals": reaction_totals
        })

    
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    

@noteBp.get('/topnote/<emoji>')
def topnote(emoji):
    try:
        note = Note.get_top_note_for_emoji(emoji)
        if not note:
            return jsonify({"status": "error", "message": "No notes found."})

        return jsonify({
            "status": "success",
            "note": note
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
