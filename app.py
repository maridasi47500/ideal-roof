from flask import Flask, render_template, request, session
import os
from yourappdb import query_db, get_db
from flask import g

app = Flask(__name__)
app.secret_key="any string"
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
init_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    user = query_db('select * from contacts')
    the_username = "anonyme"
    one_user = query_db('select * from contacts where first_name = ?',
                [the_username], one=True)
    return render_template("hey.html", users=user, one_user=one_user, the_title="my title")
@app.route("/add_one_liste_courses_nourriture", methods=["GET","POST"])
def add_one_liste_courses_nourriture():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into liste_courses_nourriture (date,name) values (:date,:name)",hey)
        user = query_db('select * from liste_courses_nourriture')

        return render_template("liste_courses_nourritureform.html", liste_courses_nourritures=user, one_user=one_user, the_title="add new liste_courses_nourriture")


    user = query_db('select * from liste_courses_nourriture')
    one_user = query_db("select * from liste_courses_nourriture limit 1", one=True)
    return render_template("liste_courses_nourritureform.html", liste_courses_nourritures=user, one_user=one_user, the_title="add new liste_courses_nourriture")

@app.route("/add_one_list_item", methods=["GET","POST"])
def add_one_list_item():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesliste_courses_nourriture= query_db("select * from liste_courses_nourriture")

        one_user = query_db("insert into list_item (liste_courses_nourriture_id,item_name) values (:liste_courses_nourriture_id,:item_name)",hey)
        user = query_db('select * from list_item')

        return render_template("list_itemform.html", list_items=user, one_user=one_user, the_title="add new list_item", touslesliste_courses_nourriture=touslesliste_courses_nourriture)


    touslesliste_courses_nourriture= query_db("select * from liste_courses_nourriture")

    user = query_db('select * from list_item')
    one_user = query_db("select * from list_item limit 1", one=True)
    return render_template("list_itemform.html", list_items=user, one_user=one_user, the_title="add new list_item", touslesliste_courses_nourriture=touslesliste_courses_nourriture)

@app.route("/add_one_user", methods=["GET","POST"])
def add_one_user():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslescountry= query_db("select * from country")

        one_user = query_db("insert into user (username,phone,email,password,country_id) values (:username,:phone,:email,:password,:country_id)",hey)
        user = query_db('select * from user')

        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        session["current_user_id"]=last_user["id"]
        for x in ['username','phone','email','password','country_id']:
            session[x]=hey[x]


        return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


    touslescountry= query_db("select * from country")

    user = query_db('select * from user')
    one_user = query_db("select * from user limit 1", one=True)
    return render_template("userform.html", users=user, one_user=one_user, the_title="add new user", touslescountry=touslescountry)


@app.route("/user_sign_out", methods=["GET","POST"])
def user_sign_out():
    if request.method == 'POST':
        session["current_user_id"]=""
        for x in ['username','phone','email','password','country_id']:
            session[x]=""
        return redirect("/")


@app.route("/user_log_in", methods=["GET","POST"])
def user_login():
    if request.method == 'POST':
        hey=request.form
        last_user = query_db("select * from user where email = ? and password = ?",[hey["email"], hey["password"]], one=True)
        try:
            session["current_user_id"]=last_user["id"]
            for x in ['username','phone','email','password','country_id']:
                session[x]=hey[x]
        except:
            return render_template("userlogin.html")
    return render_template("userlogin.html")
@app.route("/add_one_country", methods=["GET","POST"])
def add_one_country():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into country (name) values (:name)",hey)
        user = query_db('select * from country')

        return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")


    user = query_db('select * from country')
    one_user = query_db("select * from country limit 1", one=True)
    return render_template("countryform.html", countrys=user, one_user=one_user, the_title="add new country")

@app.route("/add_one_bedroom", methods=["GET","POST"])
def add_one_bedroom():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into bedroom (name) values (:name)",hey)
        user = query_db('select * from bedroom')

        return render_template("bedroomform.html", bedrooms=user, one_user=one_user, the_title="add new bedroom")


    user = query_db('select * from bedroom')
    one_user = query_db("select * from bedroom limit 1", one=True)
    return render_template("bedroomform.html", bedrooms=user, one_user=one_user, the_title="add new bedroom")

@app.route("/add_one_musicgenre", methods=["GET","POST"])
def add_one_musicgenre():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        one_user = query_db("insert into musicgenre (name) values (:name)",hey)
        user = query_db('select * from musicgenre')

        return render_template("musicgenreform.html", musicgenres=user, one_user=one_user, the_title="add new musicgenre")


    user = query_db('select * from musicgenre')
    one_user = query_db("select * from musicgenre limit 1", one=True)
    return render_template("musicgenreform.html", musicgenres=user, one_user=one_user, the_title="add new musicgenre")

@app.route("/add_one_usersharemusicstyle", methods=["GET","POST"])
def add_one_usersharemusicstyle():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesuser= query_db("select * from user")

        touslesmusicgenre= query_db("select * from musicgenre")

        one_user = query_db("insert into usersharemusicstyle (user_id,musicgenre_id) values (:user_id,:musicgenre_id)",hey)
        user = query_db('select * from usersharemusicstyle')

        return render_template("usersharemusicstyleform.html", usersharemusicstyles=user, one_user=one_user, the_title="add new usersharemusicstyle", touslesuser=touslesuser, touslesmusicgenre=touslesmusicgenre)


    touslesuser= query_db("select * from user")

    touslesmusicgenre= query_db("select * from musicgenre")

    user = query_db('select * from usersharemusicstyle')
    one_user = query_db("select * from usersharemusicstyle limit 1", one=True)
    return render_template("usersharemusicstyleform.html", usersharemusicstyles=user, one_user=one_user, the_title="add new usersharemusicstyle", touslesuser=touslesuser, touslesmusicgenre=touslesmusicgenre)

@app.route("/add_one_usersharebed", methods=["GET","POST"])
def add_one_usersharebed():

    if request.method == 'POST':

        the_username = "anonyme"
        hey=dict(request.form)


        touslesbedroom= query_db("select * from bedroom")

        touslesuser= query_db("select * from user")

        one_user = query_db("insert into usersharebed (bedroom_id,user_id) values (:bedroom_id,:user_id)",hey)
        user = query_db('select * from usersharebed')

        return render_template("usersharebedform.html", usersharebeds=user, one_user=one_user, the_title="add new usersharebed", touslesbedroom=touslesbedroom, touslesuser=touslesuser)


    touslesbedroom= query_db("select * from bedroom")

    touslesuser= query_db("select * from user")

    user = query_db('select * from usersharebed')
    one_user = query_db("select * from usersharebed limit 1", one=True)
    return render_template("usersharebedform.html", usersharebeds=user, one_user=one_user, the_title="add new usersharebed", touslesbedroom=touslesbedroom, touslesuser=touslesuser)

