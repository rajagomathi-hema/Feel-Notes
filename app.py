from flask import Flask, render_template, redirect, session
from mongoengine import connect, connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'OUGZTFDRZFÖOJLD'

try:
    connect(host="mongodb://localhost:27017/feelNotes")
    if connection.get_connection():
        print("Database Connected Successfully.")
    else:
        print("Database not Connected.")
except Exception as e:
    print({"status": "error", "message": f"Error: {str(e)}"})

from user import userBp
app.register_blueprint(userBp, url_prefix='/user')

from note import noteBp
app.register_blueprint(noteBp,url_prefix='/note')

from calmZone import calmZoneBp
app.register_blueprint(calmZoneBp,url_prefix='/calmZone')

from auth import auth_bp
app.register_blueprint(auth_bp,url_prefix='/auth')

from save import saveBp
app.register_blueprint(saveBp,url_prefix='/save')

@app.get('/')
def main():
    sessionUser = session.get('user')
    if not sessionUser:
        return redirect('/login')
    return render_template('index.html')

@app.get('/<page>')
def loadPages(page):
    sessionUser = session.get('user')
    if not sessionUser:
        return render_template('login.html')
    return render_template(f'{page}.html')

@app.context_processor
def loadData():
    sessionUser = session.get('user')
    if not sessionUser:
        return {
            'isLogin': False
        }
    
    return {
        'isLogin': True,
        'user': sessionUser
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')