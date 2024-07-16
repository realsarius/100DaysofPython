from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_API_KEY = "2a99123553f1fe4d8316deea7425df97"  # Make sure to use your actual API key
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

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
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String, nullable=True)
    img_url: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return (f"<Movie(id={self.id}, title='{self.title}', year={self.year}, "
                f"description='{self.description}', rating={self.rating}, "
                f"ranking={self.ranking}, review='{self.review}', img_url='{self.img_url}')>")

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# # CREATE TABLE
# with app.app_context():
#     db.create_all()

# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title=request.form['title']
        movie_name = title.split(" ")
        movie_name = "%20".join(movie_name)

        url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"


        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYTk5MTIzNTUzZjFmZTRkODMxNmRlZWE3NDI1ZGY5NyIsIm5iZiI6MTcyMTA2MjIxOS40NDEzMSwic3ViIjoiNjY5NTJiZTk3ZDk5YmIxYjBjYTk3NDVmIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.3lITiSgys__fAV09n5n9NfNFAR6fFHjHAb9yJzgRAKM"
        }   

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results = response.json()
        movies_list = results["results"]
        
        return render_template("select.html", movies=movies_list)

    return render_template('add.html')

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        
        if response.status_code == 200:
            data = response.json()
            new_movie = Movie(
                title=data["title"],
                year=data["release_date"].split("-")[0],
                img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}" if data.get('poster_path') else None,
                description=data["overview"]
            )
            db.session.add(new_movie)
            db.session.commit()

            return redirect(url_for("edit", movie_title=new_movie.title))
        

    return redirect(url_for("home"))


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
        return redirect(url_for('home'))

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
