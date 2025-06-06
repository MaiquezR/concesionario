import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:admin@localhost:5432/flask_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(25), nullable=False)

    def __init__(self, make, model, color):

        self.make = make
        self.model = model
        self.color = color


class FlaskQueries:

    @app.route("/")
    def index():

        cars = Car.query.all()

        return render_template("index.html", cars=cars)

    @app.route("/add", methods=["POST"])
    def create():

        make = (request.form["make"],)
        model = (request.form["model"],)
        color = (request.form["color"],)

        new_car = Car(make=make, model=model, color=color)

        db.session.add(new_car)
        db.session.commit()

        return redirect(url_for("index"))

    @app.route("/update", methods=["POST"])
    def update():

        id = request.form["id"]

        car_to_update = Car.query.get_or_404(id)

        make = request.form["make"]
        model = request.form["model"]
        color = request.form["color"]

        car_to_update.make = make
        car_to_update.model = model
        car_to_update.color = color

        db.session.add(car_to_update)
        db.session.commit()

        return redirect(url_for("index"))

    # The delete route deletes a car by id
    @app.route("/delete", methods=["POST"])
    def deletecar():

        id = request.form["id"]

        car_to_delete = Car.query.get_or_404(id)

        db.session.delete(car_to_delete)
        db.session.commit()

        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
