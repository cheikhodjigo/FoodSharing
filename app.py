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
        db = Database()
        offers = db.get_all_offers()
        return render_template('Navigate.html', year=now, offers=offers)


@app.route('/successInscription')
def success_inscription_page():
    return render_template('Done_Inscription.html', year=now)


@app.route('/profile')
def access_profile():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        user_infos = db.get_user_by_id(session.get('id'))
        return render_template('my_profile.html', year=now, user_infos=user_infos)


@app.route('/offer/<id>')
def access_offer_info(id):
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        offer_info = db.get_offer_by_id(id)
        db1 = Database()                    # set a method to close the database
        user=db1.get_user_by_id(offer_info[2])
        return render_template('offer.html', year=now, offer_info=offer_info, user=user)


@app.route('/change_password')
def change_password():
    if session.get("id") is None:
        return redirect('/')
    else:
        return render_template('change_password.html', year=now)


@app.route('/offer_created')
def access_offer_created():
    if session.get("id") is None:
        return redirect('/')
    else:
        return render_template('success_offer_created.html', year=now)


@app.route('/my_offers')
def access_my_offers_created():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        user_offers = db.get_offers(session.get('id'))
        return render_template('my_offers.html', year=now, user_offers=user_offers)


@app.route('/add_offer', methods=['POST', 'GET'])
def add_offer():
    if session.get("id") is None:
        return redirect('/')
    else:
        if request.method == 'GET':
            db = Database()
            categories = db.get_categories()
            return render_template('add_offer.html', year=now, categories=categories)
        else:
            categorie = request.form['categorie']
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            user_id = session.get('id')
            db = Database()
            db.add_offer(categorie, user_id, title, description, price)
            return "1"


@app.route('/login', methods=['POST'])
def check_user():
    mail = request.form["email"]
    password = request.form["password"]
    db = Database()
    result = db.get_user_by_mail(mail)
    if result is None:
        return "0"
    elif check_password_hash(result[2], password):
        session["id"] = result[0]
        return "1"
    else:
        return "2"


@app.route('/delete_user_offer', methods=['POST'])
def delete_user_offer():
    if session.get("id") is None:
        return redirect('/')
    else:
        offer_id = request.form['offer_id']
        db = Database()
        db.delete_offer_from_user(offer_id)
        return "1"


@app.route('/disconnect', methods=['GET'])
def disconnect_user():
    if session.get('id') is not None:
        session.pop('id', None)
    return redirect('/')
