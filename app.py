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
        return render_template('login.html', year=now)
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
            db.disconnect()
            return "1"


@app.route('/accueil')
def home_page():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        offers = db.get_all_offers()
        categories = db.get_categories()
        role = session.get("role")
        db.disconnect()
        return render_template('home.html', year=now, offers=offers, categories=categories, role=role[0])


@app.route('/admin')
def home_page_admin():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        offers = db.get_all_offers()
        categories = db.get_categories()
        db.disconnect()
        return render_template('home_admin.html', year=now, offers=offers, categories=categories)


@app.route('/successInscription')
def success_inscription_page():
    return render_template('success_subscribe.html', year=now)


@app.route('/profile')
def access_profile():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        user_infos = db.get_user_by_id(session.get('id'))
        role = session.get("role")
        db.disconnect()
        return render_template('my_profile.html', year=now, user_infos=user_infos, role=role[0])


@app.route('/offer/<id>')
def access_offer_info(id):
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        offer_info = db.get_offer_by_id(id)
        user = db.get_user_by_id(offer_info[2])
        role = session.get("role")
        db.disconnect()
        return render_template('offer.html', year=now, offer_info=offer_info, user=user, role=role[0])


@app.route('/change_password')
def change_password():
    if session.get("id") is None:
        return redirect('/')
    else:
        role = session.get("role")
        return render_template('change_password.html', year=now, role=role[0])


@app.route('/offer_created')
def access_offer_created():
    if session.get("id") is None:
        return redirect('/')
    else:
        role = session.get("role")
        return render_template('success_offer_created.html', year=now, role=role[0])


@app.route('/my_offers')
def access_my_offers_created():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        user_offers = db.get_offers(session.get('id'))
        role = session.get("role")
        db.disconnect()
        return render_template('my_offers.html', year=now, user_offers=user_offers, role=role[0])


@app.route('/manage_offers')
def manage_system_offers():
    if session.get("id") is None:
        return redirect('/')
    else:
        if session.get("role")[0] == "Administrateur":
            db = Database()
            offers = db.get_all_offers()
            role = session.get("role")
            db.disconnect()
            return render_template('manage_offers.html', year=now, offers=offers, role=role[0])
        else:
            return redirect('/')


@app.route('/manage_users')
def manage_system_users():
    if session.get("id") is None:
        return redirect('/')
    else:
        if session.get("role")[0] == "Administrateur":
            db = Database()
            users = db.get_all_users_except_actual(session.get("id"))
            role = session.get("role")
            db.disconnect()
            return render_template('manage_users.html', year=now, users=users, role=role[0])
        else:
            return redirect('/')


@app.route('/add_offer', methods=['POST', 'GET'])
def add_offer():
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        if request.method == 'GET':
            categories = db.get_categories()
            role = session.get("role")
            db.disconnect()
            return render_template('add_offer.html', year=now, categories=categories, role=role[0])
        else:
            categorie = request.form['categorie']
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            user_id = session.get('id')
            db.add_offer(categorie, user_id, title, description, price)
            db.disconnect()
            return "1"


@app.route('/delete_user_offer', methods=['POST'])
def delete_user_offer():
    if session.get("id") is None:
        return redirect('/')
    else:
        offer_id = request.form['offer_id']
        db = Database()
        db.delete_offer_from_user(offer_id)
        db.disconnect()
        return "1"


@app.route('/delete_offer/<offer_id>')
def delete_offer(offer_id):
    if session.get("id") is None:
        return redirect('/')
    else:
        db = Database()
        db.delete_offer_from_user(offer_id)
        db.disconnect()
        return redirect("/manage_offers")


@app.route('/update_user_infos', methods=['POST'])
def update_user_infos():
    if session.get("id") is None:
        return redirect('/')
    else:
        user_id = session.get('id')
        fname = request.form['change-fname']
        lname = request.form['change-lname']
        phone = request.form['change-phone']
        mail = request.form['change-email']
        db = Database()
        db.change_user_information(fname, lname, mail, phone, user_id)
        db.disconnect()
        return render_template("success_update_message.html")


@app.route("/search_results", methods=['GET'])
def find_results():
    value = request.args.get('search_value')
    categorie = request.args.get('categorie')
    db = Database()
    offers = db.search_offers(value, categorie)
    categories = db.get_categories()
    role = session.get("role")
    db.disconnect()
    return render_template('result_research.html', year=now, offers=offers, categories=categories, role=role[0])


@app.route("/change_user_status/<user_id>", methods=['GET'])
def change_user_status(user_id):
    user_status = request.args.get('p')
    db = Database()
    db.change_user_status(user_id, user_status)
    db.disconnect()
    return redirect("/manage_users")


@app.route('/login', methods=['POST'])
def check_user():
    mail = request.form["username"]
    password = request.form["password"]
    db = Database()
    result = db.get_user_by_mail(mail)
    if result is None:
        db.disconnect()
        return "0"
    elif check_password_hash(result[2], password):
        if result[3] == 'Inactif':
            return "4"
        else:
            session["id"] = result[0]
            role = db.get_user_role(result[0])
            db.disconnect()
            session["role"] = role
            return "2"
    else:
        return "3"


@app.route('/disconnect', methods=['GET'])
def disconnect_user():
    if session.get('id') is not None:
        session.pop('id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5001, debug = False)