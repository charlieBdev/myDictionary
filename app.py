import os
import requests
import urllib.parse

import os
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///myDictionary.db")

# Config app
app = Flask(__name__)

# Config session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
@login_required
def index():

    userID = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", userID)[0]["username"]
    words = db.execute("SELECT * FROM words WHERE userID = ? GROUP BY word", userID)

    return render_template("index.html", username=username, words=words)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Username is required!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Password is required!")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


def apology(message):
    return render_template("apology.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # if no password is entered
        if not username:
            return apology("Username is required!")
        elif not password:
            return apology("Password is required!")
        elif not confirmation:
            return apology("Password confirmation is required!")

        if password != confirmation:
            return apology("Passwords do not match!")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return redirect('/')
        except:
            return apology("Username already exists!")

    # if GET?
    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    elif request.method == "POST":

        userID = session["user_id"]

        word = request.form.get("word")
        definition = request.form.get("definition")
        partOfSpeech = request.form.get("partOfSpeech")
        sentence = request.form.get("sentence")
        notes = request.form.get("notes")

        if word:
            try:
                db.execute("INSERT INTO words (userID, word, definition, partOfSpeech, sentence, notes) VALUES (?, ?, ?, ?, ?, ?)", userID, word, definition, partOfSpeech, sentence, notes)
                return redirect('/')
            except:
                return apology("Error")
        else:
            return apology("Enter a word!")


@app.route("/view", methods=["GET"])
def view():

    wordID = request.form.get("wordID")

    entry = db.execute("SELECT * FROM words WHERE id = ?", wordID)
    definition = entry[0]['definition']
    partOfSpeech = entry[0]['partOfSpeech']
    sentence = entry[0]['sentence']
    notes = entry[0]['notes']

    return render_template("view.html", wordID=wordID, word=word, definition=definition, partOfSpeech=partOfSpeech, sentence=sentence, notes=notes)


@app.route("/delete", methods=["POST"])
def delete():
    wordID = request.form.get("wordID")

    try:
        db.execute("DELETE FROM words WHERE id = ?", wordID)
    except:
        return apology("Deletion error!")

    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    wordID = request.form.get("wordID")

    entry = db.execute("SELECT * FROM words WHERE id = ?", wordID)
    word = entry[0]['word']
    definition = entry[0]['definition']
    partOfSpeech = entry[0]['partOfSpeech']
    sentence = entry[0]['sentence']
    notes = entry[0]['notes']

    return render_template("edit.html", wordID=wordID, word=word, definition=definition, partOfSpeech=partOfSpeech, sentence=sentence, notes=notes)

@app.route("/saveEdit", methods=["POST"])
def saveEdit():

    wordID = request.form.get("wordID")

    word = request.form.get("word")
    definition = request.form.get("definition")
    partOfSpeech = request.form.get("partOfSpeech")
    sentence = request.form.get("sentence")
    notes = request.form.get("notes")

    if word:
        try:
            db.execute("UPDATE words SET word = ?, definition = ?, partOfSpeech = ?, sentence = ?, notes = ? WHERE id = ?", word, definition, partOfSpeech, sentence, notes, wordID)
            return redirect('/')
        except:
            return apology("Error")
    else:
        return apology("Enter a word!")