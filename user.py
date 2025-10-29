from flask import Flask, request, jsonify ,render_template
from models import User
app = Flask(__name__)

@app.post('/new')
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


@app.put("/update")
def updateStudent():
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
    
    
@app.get('/get')
def main():
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

        return jsonify({"status": "success", "message": "User retrived","data":userList} )
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    
