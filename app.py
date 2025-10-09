import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import items
import users
import re
import csv
from datetime import datetime

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

def datetimeformat(value):
    if not value:
        return ""
    try:
        dt = datetime.strptime(value, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        return value


@app.route("/search_item")
def search_item():
    query = request.args.get("query")
    if query:
        results = items.search_items(query)
    else:
        query = ""
        results = []
    return render_template("search_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/new_item")
def new_item():
    require_login()
    municipalities = get_municipalities()
    species = get_species()
    return render_template("new_item.html", municipalities=municipalities, species=species)

def get_species(filename="species.csv"):
    species = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            species.append(row["classificationName"])
    return species

def get_municipalities(filename="municipalities.csv"):
    municipalities = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            municipalities.append(row["classificationName"])
    return municipalities

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()    
    species = request.form["species"]
    if species not in get_species():
        abort(403, "Lajin nimi ei kelpaa!")
    date_str = request.form["date"]
    try:
        from datetime import datetime
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        abort(403, "Virheellinen päivämäärä!")
    if date > datetime.today().date():
        abort(403, "Päivämäärä ei voi olla tulevaisuudessa!")
    amount = request.form["amount"]
    if not amount or not re.search("^[1-9][0-9]{0,9}$",amount):
        abort(403)
    municipality = request.form["municipality"]
    if not municipality or len(municipality) > 20:
        abort(403)
    place = request.form["place"]
    if not place or len(place) > 50:
        abort(403)
    description = request.form["description"]
    if len(description) > 500:
        abort(403)
    user_id = session["user_id"]

    items.add_item(species, date, amount, place, municipality, description, user_id)
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/remove_item/<int:item_id>", methods=["GET","POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]
    if not item_id:
        abort(404)
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    species = request.form["species"]
    if species not in get_species():
        abort(403)
    amount = request.form["amount"]
    if not amount or not re.search("^[1-9][0-9]{0,9}$",amount):
        abort(403)
    municipality = request.form["municipality"]
    if municipality not in get_municipalities():
        abort(403)
    place = request.form["place"]
    if not place or len(place) > 50:
        abort(403)
    description = request.form["description"]
    if len(description) > 500:
        abort(403)

    items.update_item(item_id, species, amount, place, municipality, description)
    return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    user_id = users.check_login(username, password)
        
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

app.jinja_env.filters['datetimeformat'] = datetimeformat