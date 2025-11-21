from flask import request, jsonify, Blueprint
from models import User

userBp = Blueprint('userBp', __name__)

@userBp.post('/new')
def newUser():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data('password')
        phoneNumber = data('phoneNumber')   

        if not name or not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."})
            
        User(
            name = name,
            email = email,
            password = password,
            phoneNumber =phoneNumber
        ).save()

        return jsonify({"status": "success", "message": "User Added Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})


@userBp.put("/update")
def updateUser():
    try:
        id = request.args.get("id")
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data('password')
        phoneNumber = data('phoneNumber')

        user = User.objects(id=id).first()
        
        if not user:
            return jsonify({"status": "error", "message": "User not found"})
        
        user.name = name
        user.email = email
        user.password = password
        user.phoneNumber = phoneNumber
        user.save()

        return jsonify({"status": "success", "message": "User details updated"})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    
    
@userBp.get('/getAll')
def getAllUser():
    try:
        users = User.objects()

        userList = []
    
        for user in users:
            data = {
                "id":user.id,
                "name": user.name, 
                "email":  user.email, 
                "password": user.password,
                "phoneNumber": user.phoneNumber,
                "addedTime": user.addedTime,
                "updatedTime":user.updatedTime
            }

            userList.append(data)

        return jsonify({"status": "success", "message": "Users retrived succeessfully","data":userList} )
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
        
@userBp.get("/getSingle")
def getSingleUser():
    try:

        id = request.args.get("id")

        user = User.objects(id = id).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found"})
        
        userData = {
            "id":user.id,
            "name": user.name, 
            "email": user.email, 
            "password": user.password,
            "phoneNumber":user.phoneNumber
        }

        return jsonify({"status": "success", "message": "User retrived succeessfully", "data": userData}) 

    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})


@userBp.delete("/delete")
def deleteUser():
    try:
        id = request.args.get("id")

        user = User.objects(id = id).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found"})
        
        user.delete()

        return jsonify({"status": "success", "message": "User found and removed from users list."}) 
    except Exception as e: 
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})