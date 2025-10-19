import re
import csv
from math import ceil
from datetime import datetime
from flask import abort, make_response, redirect, render_template, request, session
from app import app
import items
from routes.user_routes import require_login, check_csrf

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
    page = request.args.get("page", 1, type=int)
    per_page = 5
    item = items.get_item(item_id)
    if not item:
        abort(404)
    images = items.get_images(item_id)
    all_comments = items.get_comments(item_id)

    total_count = len(all_comments)
    total_pages = ceil(total_count / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    paged_comments = all_comments[start:end]

    return render_template("show_item.html",
                           item=item, images=images,
                           comments=paged_comments,page=page,
                           total_pages=total_pages)

@app.route("/remove_comment/<int:comment_id>", methods=["GET","POST"])
def remove_comment(comment_id):
    require_login()

    comment = items.get_comment(comment_id)
    if not comment:
        abort(404)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        item = items.get_item(comment["item_id"])
        return render_template("remove_comment.html", comment=comment, item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_comment(comment_id)
        return redirect("/item/" + str(comment["item_id"]))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    images = items.get_images(item_id)
    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".jpg"):
        return "VIRHE: väärä tiedostomuoto"

    image = file.read()
    if len(image) > 100 * 1024:
        return "VIRHE: liian suuri kuva"

    items.add_image(item_id, image)
    return redirect("/images/" + str(item_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    for image_id in request.form.getlist("image_id"):
        items.remove_image(item_id, image_id)

    return redirect("/images/" + str(item_id))

@app.route("/new_item")
def new_item():
    require_login()
    municipalities = get_municipalities()
    species = get_species()
    return render_template("new_item.html", municipalities=municipalities, species=species)

def get_species(filename="species.csv"):
    species = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            species.append(row["classificationName"])
    return species

def get_municipalities(filename="municipalities.csv"):
    municipalities = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            municipalities.append(row["classificationName"])
    return municipalities

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    species = request.form["species"]
    if species not in get_species():
        return render_template("new_item.html", error="Lajin nimi ei kelpaa!")
    date_str = request.form["date"]
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return render_template("new_item.html", error="Virheellinen päivämäärä!")
    if date > datetime.today().date():
        return render_template("new_item.html", error="Päivämäärä ei voi olla tulevaisuudessa!")
    amount = request.form["amount"]
    if not amount or not re.search("^[1-9][0-9]{0,9}$",amount):
        return render_template("new_item.html", error="Määrä ei ole kelvollinen!")
    municipality = request.form["municipality"]
    if municipality not in get_municipalities():
        return render_template("new_item.html", error="Paikkakunnan nimi ei kelpaa!")
    place = request.form["place"]
    if not place or len(place) > 50:
        return render_template("new_item.html",
                        error="Havaintopaikkaa ei ole kirjattu tai se on yli 50 merkkiä pitkä!")
    description = request.form["description"]
    if len(description) > 500:
        return render_template("new_item.html", error="Kuvaus on liian pitkä!")
    user_id = session["user_id"]

    items.add_item(species, date, amount, place, municipality, description, user_id)
    return redirect("/")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    comment = request.form["comment"]
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, comment)
    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    municipalities = get_municipalities()
    species = get_species()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item, species=species, municipalities=municipalities)

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
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    if not item_id:
        abort(404)
    item = items.get_item(item_id)
    if item["user_id"] != session["user_id"]:
        abort(403)

    species = request.form["species"]
    if species not in get_species():
        return render_template("new_item.html", error="Lajin nimi ei kelpaa!")
    date_str = request.form["date"]
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return render_template("new_item.html", error="Virheellinen päivämäärä!")
    if date > datetime.today().date():
        return render_template("new_item.html", error="Päivämäärä ei voi olla tulevaisuudessa!")
    amount = request.form["amount"]
    if not amount or not re.search("^[1-9][0-9]{0,9}$",amount):
        return render_template("new_item.html", error="Määrä ei ole kelvollinen!")
    municipality = request.form["municipality"]
    if municipality not in get_municipalities():
        return render_template("new_item.html", error="Paikkakunnan nimi ei kelpaa!")
    place = request.form["place"]
    if not place or len(place) > 50:
        return render_template("new_item.html", error="Havaintopaikkaa ei ole kirjattu tai se on yli 50 merkkiä pitkä!")
    description = request.form["description"]
    if len(description) > 500:
        return render_template("new_item.html", error="Kuvaus on liian pitkä!")

    items.update_item(item_id, species, date, amount, place, municipality, description)
    return redirect("/item/" + str(item_id))
