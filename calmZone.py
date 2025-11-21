from flask import request, jsonify, Blueprint
from models import CalmZone

calmZoneBp = Blueprint('calmZoneBp', __name__)

@calmZoneBp.post('/new')
def newCalmZone():
    try:
        data = request.get_json()

        content = data.get('content')
        
        
        if not content :
            return jsonify({"status": "error", "message": "CalmZone fields required."})
            
        CalmZone (
            content = content,
            ).save()

        return jsonify({"status": "success", "message": "CalmZone created Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    

@calmZoneBp.get('/getAll')
def getAllCalmZone():
    try:
        calmZones = CalmZone.objects()

        calmZoneList = []
    
        for calmZone in calmZones:
            data = {
                "id":calmZone.id,
                "content":calmZone.content,
                "addedTime": calmZone.addedTime,
                "updatedTime":calmZone.updatedTime
            }

            calmZoneList.append(data)

        return jsonify({"status": "success", "message": " CalmZone retrived succeessfully","data":calmZoneList} )
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
        

@calmZoneBp.delete("/delete")
def deleteCalmZone():
    try:
        id = request.args.get("id")

        calmZone =CalmZone.objects(id = id).first()

        if not calmZone:
            return jsonify({"status": "error", "message": "CalmZone not found"})
        
        calmZone.delete()

        return jsonify({"status": "success", "message": " CalmZone found and removed from CalmZone list."}) 
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})