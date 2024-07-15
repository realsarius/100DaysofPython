from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String, nullable=False)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (f"<Movie(id={self.id}, title='{self.title}', year={self.year}, "
                f"description='{self.description}', rating={self.rating}, "
                f"ranking={self.ranking}, review='{self.review}', img_url='{self.img_url}')>")

second_movie = Movie(
    title="Avatar The Way of Water",
    year=2022,
    description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    rating=7.3,
    ranking=9,
    review="I liked the water.",
    img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
)

# CREATE TABLE
# with app.app_context():
#     db.create_all()

# with app.app_context():
#     db.session.add(second_movie)
#     db.session.commit()

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        with app.app_context():
            new_movie = Movie(
            title=request.form['title'],
            year=request.form['year'],
            description=request.form['description'],
            rating=request.form['rating'],
            ranking=request.form['ranking'],
            review=request.form['review'],
            img_url=request.form['img_url'])
            db.session.add(new_movie)
            db.session.commit()
    return render_template('add.html')

@app.route('/delete')
def delete_movie():
    movie_title = request.args.get('movie_title')
    print(f"Deleting movie: {movie_title}")

    movie_to_delete = Movie.query.filter_by(title=movie_title).first()
    
    if movie_to_delete is None:
        print("Movie not found in the database.")
        return redirect(url_for('home'))

    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



@app.route("/edit", methods=['GET', 'POST'])
def edit():
    movie_title = request.args.get('movie_title')
    print(f"Movie title received: {movie_title}") 

    selected_movie = Movie.query.filter_by(title=movie_title).first()
    if not selected_movie:
        print("Movie not found in the database.")
        return redirect(url_for('home'))  # Redirect or handle the error

    if request.method == 'POST':
        selected_movie.rating = request.form['rating']
        selected_movie.review = request.form['review']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=selected_movie)


@app.route("/")
def home():
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
        all_movies = result.scalars().all()
        print(all_movies)
    return render_template("index.html", all_movies=all_movies)

if __name__ == '__main__':
    app.run(debug=True)
