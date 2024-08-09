from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, URL
from forms import CafeForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = 'your_secret_key'

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    __tablename__ = "cafe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    map_url: Mapped[str] = mapped_column(unique=True)
    img_url: Mapped[str] = mapped_column(unique=True)
    location: Mapped[str] = mapped_column()
    has_sockets: Mapped[bool] = mapped_column()
    has_toilet: Mapped[bool] = mapped_column()
    has_wifi: Mapped[bool] = mapped_column()
    can_take_calls: Mapped[bool] = mapped_column()
    seats: Mapped[str] = mapped_column()
    coffee_price: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
         return f"Cafe(id={self.id!r}, name={self.name!r}, location={self.location!r})"

with app.app_context():
    db.create_all()

@app.route('/api/cafes', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm(request.form)
    if form.validate_on_submit():
        try:
            new_cafe = Cafe(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets=form.has_sockets.data,
                has_toilet=form.has_toilet.data,
                has_wifi=form.has_wifi.data,
                can_take_calls=form.can_take_calls.data,
                seats=form.seats.data,
                coffee_price=form.coffee_price.data
            )

            db.session.add(new_cafe)
            db.session.commit()

            return make_response(jsonify({
                'id': new_cafe.id,
                'name': new_cafe.name,
                'map_url': new_cafe.map_url,
                'img_url': new_cafe.img_url,
                'location': new_cafe.location,
                'has_sockets': new_cafe.has_sockets,
                'has_toilet': new_cafe.has_toilet,
                'has_wifi': new_cafe.has_wifi,
                'can_take_calls': new_cafe.can_take_calls,
                'seats': new_cafe.seats,
                'coffee_price': new_cafe.coffee_price
            }), 201)
        except Exception as e:
            print(f"An error occurred: {e}")
            return make_response(jsonify({'error': 'An error occurred while adding the cafe'}), 500)
    else:
        return make_response(jsonify({'errors': form.errors}), 400)
    return


@app.route('/api/cafes/<int:id>', methods=['GET'])
def get_cafe(id):
    try:
        cafe = Cafe.query.get_or_404(id)
        cafe_data = {
            'id': cafe.id,
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'has_sockets': cafe.has_sockets,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'can_take_calls': cafe.can_take_calls,
            'seats': cafe.seats,
            'coffee_price': cafe.coffee_price
        }
        return make_response(jsonify(cafe_data), 200)
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'An error occurred while retrieving the cafe'}), 500)

@app.route('/api/cafes', methods=['GET'])
def get_all_cafes():
    try:
        cafes = Cafe.query.all()
        if cafes:
            cafes_list = [
                {
                    'id': cafe.id,
                    'name': cafe.name,
                    'map_url': cafe.map_url,
                    'img_url': cafe.img_url,
                    'location': cafe.location,
                    'has_sockets': cafe.has_sockets,
                    'has_toilet': cafe.has_toilet,
                    'has_wifi': cafe.has_wifi,
                    'can_take_calls': cafe.can_take_calls,
                    'seats': cafe.seats,
                    'coffee_price': cafe.coffee_price
                }
                for cafe in cafes
            ]
            return make_response(jsonify({'cafes': cafes_list}), 200)
        else:
            return make_response(jsonify({'error': 'No cafes found'}), 404)
    except Exception as e:
        print(f"An error occurred: {e}")
        return make_response(jsonify({'error': 'An error occurred while retrieving cafes'}), 500)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)