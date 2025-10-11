from app import app
from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session
import sqlite3
import users

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("register.html", error="Salasanat eivät ole samat!")    
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Tunnus on jo varattu!")
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
        return render_template("login.html", error="Väärä tunnus tai salasana!")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
