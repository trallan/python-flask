import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)

SPORTS = [
    "Basketball",
    "Soccer",
    "Ultimate Frisbee",
]

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("test.db")
        g.db.row_factory = sqlite3.Row
    return g.db


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return render_template("greet.html", name=request.form.get("name"))
    else:
        return render_template("index.html", sports=SPORTS)
    
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    if not name:
        return render_template("error.html", message="Missing name")

    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")
   
    db = get_db()
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", (name, sport))
    db.commit()

    return render_template("success.html", name=name, sport=sport)


@app.route("/registrants")
def registrants():
    db = get_db()
    registrants = db.execute("SELECT name, sport FROM registrants")
    return render_template("registrants.html", registrants=registrants)