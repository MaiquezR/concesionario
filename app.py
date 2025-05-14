from logging import debug
from re import DEBUG
from flask import Flask, render_template, request, redirect, url_for
import psycopg

# List of SQL queries
CREATE_CARS_TABLE = (
    "CREATE TABLE IF NOT EXISTS cars (id serial PRIMARY KEY,"
    "make varchar (150) NOT NULL,"
    "model varchar (150) NOT NULL,"
    "color varchar (25),"
    "sold BIT DEFAULT B'0'"
    ");"
)

GET_ALL_CARS = "SELECT * FROM cars"

GET_CAR_BY_ID = "SELECT * FROM cars WHERE id=%s"

# GET_CARS_FILTERED = "SELECT * FROM cars WHERE "

SELL_CAR = "UPDATE cars SET sold='1' WHERE id=%s"

INSERT_NEW_CAR = "INSERT INTO cars (make, model, color) VALUES (%s, %s, %s)"

UPDATE_CAR = "UPDATE cars SET make=%s, model=%s, color=%s WHERE id=%s"

DELETE_CAR = "DELETE FROM cars WHERE id=%s"


app = Flask(__name__)

conn = psycopg.connect(
    host="localhost",
    dbname="flask_db",
    user="postgres",
    password="root",
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Creating new table and first insert
cur.execute(CREATE_CARS_TABLE)
cur.execute(INSERT_NEW_CAR, ("citroen", "c3", "grey"))

# Commit changes
conn.commit()

if conn:
    cur.close()
    conn.close()


@app.route("/")
def index():

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()

    cur.execute(GET_ALL_CARS)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", data=data)


@app.route("/getbyid", methods=["GET"])
def getcarbyid():

    id = request.form["id"]

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()
    cur.execute(GET_CAR_BY_ID, (id,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("index"))


@app.route("/add", methods=["POST"])
def create():

    make = request.form["make"]
    model = request.form["model"]
    color = request.form["color"]

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()
    cur.execute(INSERT_NEW_CAR, (make, model, color))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():

    id = request.form["id"]
    make = request.form["make"]
    model = request.form["model"]
    color = request.form["color"]

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()
    cur.execute(UPDATE_CAR, (make, model, color, id))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("index"))


@app.route("/sell", methods=["POST"])
def sellcar():

    id = request.form["id"]

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()

    cur.execute(SELL_CAR, (id,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("index"))

    # @app.route("/filter", methods=["GET"])
    # def getcarfilter():

    #     id = request.form["id"]
    #     filter = request.form["filter"]

    # cur = conn.cursor()


#     cur.execute(GET_CARS_FILTERED, (filter, id))

#     conn.commit()

#     cur.close()
#     conn.close()

#     return render_template("index.html")


# The delete route deletes a car by id
@app.route("/delete", methods=["POST"])
def deletecar():

    id = request.form["id"]

    conn = psycopg.connect(
        host="localhost",
        dbname="flask_db",
        user="postgres",
        password="root",
    )

    cur = conn.cursor()

    cur.execute(DELETE_CAR, (id,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
