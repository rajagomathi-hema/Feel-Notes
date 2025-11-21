from flask import Blueprint, jsonify, request, session
from models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.post('/register')
def register():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phoneNumber = data.get('phoneNumber')   

        if not name or not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."})
            
        
        user = User.objects(email=email).first()
        if user:
            return jsonify({"status": "error", "message": "User already registered."})
        
        newUser = User(
            name = name,
            email = email,
            password = password,
            phoneNumber =phoneNumber
        )
        newUser.save()

        session['user'] = {
            'id': newUser.id,
            'name': newUser.name,
            'email': newUser.email
        }

        return jsonify({"status": "success", "message": "User Registered Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    

@auth_bp.post('/login')
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "error", "message": "All fields are required."})
            
        
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found please register to continue."})
        
        if user.password != password:
            return jsonify({"status": "error", "message": "Incorrect Password."})
        
        session['user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        return jsonify({"status": "success", "message": "User login Successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})
    

@auth_bp.get('/logout')
def logout():
    try:
        user = session.get('user')
        if not user:
            return jsonify({"status": "error", "message": "Unauthorized Access! Please login to logout."})
        session.clear()
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {str(e)}"})