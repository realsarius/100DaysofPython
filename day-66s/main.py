from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import requests
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary
        
        #Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random')
def random_page():
    count = Cafe.query.count()
    if count == 0:
        return jsonify({"error": "No cafes available"}), 404
    
    random_number = random.randint(1, count)
    
    cafe = Cafe.query.get_or_404(random_number)
    
    # cafe_data = {
    #     "id": cafe.id,
    #     "name": cafe.name,
    #     "map_url": cafe.map_url,
    #     "img_url": cafe.img_url,
    #     "location": cafe.location,
    #     "seats": cafe.seats,
    #     "has_toilet": cafe.has_toilet,
    #     "has_wifi": cafe.has_wifi,
    #     "has_sockets": cafe.has_sockets,
    #     "can_take_calls": cafe.can_take_calls,
    #     "coffee_price": cafe.coffee_price,
    # }
    
    print(cafe.name)
    return jsonify({"message": "success", "cafe": cafe.to_dict()}), 200

@app.route('/all')
def all_cafes_page():
    count = Cafe.query.count()
    if count == 0:
        return jsonify({"error": "No cafes available"}), 404
    cafes = Cafe.query.all()
    cafes_list = []
    for cafe in cafes:
        cafes_list.append(cafe.to_dict())

    print(cafes_list)
    return jsonify({'message': 'success', 'status': 200, 'cafes': cafes_list}), 200

@app.route('/search')
def search_cafe_page():
    cafes_in_the_area = Cafe.query.filter(Cafe.location == request.args.get('location'))    
    
    cafes_in_the_area_list = []
    for cafe in cafes_in_the_area:
        cafes_in_the_area_list.append(cafe.to_dict())

    if not cafes_in_the_area_list:
        return jsonify({'message': 'failure', 'status': 404, "cafes": "No cafe(s) in the location"}), 404

    return jsonify({'message': 'success', 'status': 200, 'cafes': cafes_in_the_area_list}), 200

# HTTP POST - Create Record
@app.route("/add", methods=['POST'])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"))

    db.session.add(new_cafe)
    db.session.commit()

    return jsonify({'message': 'success', 'status': 200, 'cafe': new_cafe.to_dict()}), 200

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.get_or_404(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

# HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    the_cafe = Cafe.query.get(cafe_id)
    
    if the_cafe is None:
        return jsonify({'error': 'Cafe not found', 'status': 404}), 404
    
    db.session.delete(the_cafe)
    db.session.commit()

    return jsonify({'message': 'success', 'status': 200, 'cafe': the_cafe.to_dict()}), 200

if __name__ == '__main__':
    app.run(debug=True)
