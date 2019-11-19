from flask import Flask, render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from database import Database


app = Flask(__name__)
app.secret_key = 'my secret key'
now = datetime.datetime.now().year


@app.route('/')
def get_login_page():
    if session.get('id') is None:
        return render_template('Home.html', year=now)
    else:
        return redirect('/accueil')


@app.route('/inscription', methods=['POST', 'GET'])
def log_into_the_system():
    if request.method == 'GET':
        return render_template('Inscription.html', year=now)
    else:
        passw = request.form['password']
        confp = request.form['confpassword']
        if passw != confp:
            return "0"
        else:
            name = request.form['nom']
            first_name = request.form['prenom']
            mail = request.form['mail']
            db = Database()
            db.add_user(first_name, name, mail, generate_password_hash(passw))
            return "1"


@app.route('/accueil')
def home_page():
    if session.get("id") is None:
        return redirect('/')
    else:
        return render_template('Navigate.html', year=now)


@app.route('/successInscription')
def success_inscription_page():
    return render_template('Done_Inscription.html', year=now)


@app.route('/profile')
def access_profile():
    return render_template('my_profile.html', year=now)


@app.route('/change_password')
def change_password():
    return render_template('change_password.html', year=now)


@app.route('/add_offer')
def add_offer():
    return render_template('add_offer.html', year=now)


@app.route('/login', methods=['POST'])
def check_user():
    mail = request.form["email"]
    password = request.form["password"]
    db = Database()
    result = db.get_user(mail)
    if result is None:
        return "0"
    elif check_password_hash(result[2], password):
        session["id"] = result[0]
        return "1"
    else:
        return "2"


@app.route('/disconnect', methods=['GET'])
def disconnect_user():
    if session.get('id') is not None:
        session.pop('id', None)
    return redirect('/')
