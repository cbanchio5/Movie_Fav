from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import sqlite3
from forms import EditForm, AddForm
MOVIE_API_KEY= 'c21defb3266bac810145a6f986a0bac3'
API_ENDPOINT='https://api.themoviedb.org/3/search/movie'
ENDPOINT_2='https://api.themoviedb.org/3/movie/'

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# db = sqlite3.connect("movie-collection.db")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collection.db'
db = SQLAlchemy(app)



class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    description = db.Column(db.String())
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String())
    img_url = db.Column(db.String)

    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()


# new_movie = Movies(title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
# db.session.add(new_movie)
# db.session.commit()




@app.route("/")
def home():

    movies = Movies.query.order_by(Movies.rating).all()
    for i in range(len(movies)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        movies[i].ranking = len(movies) - i
    return render_template("index.html", data=movies)


@app.route('/edit/<id>', methods=["GET", "POST"])
def edit(id):
    if request.method == "GET":
        form = EditForm(meta={'csrf': False})
        movie_to_update = Movies.query.get(id)
        return render_template('edit.html', form=form, movie=movie_to_update)
    else:
        response = request.form.to_dict()
        movie_to_update = Movies.query.get(id)
        if response['rating'] != "":
            movie_to_update.rating = response['rating']
        if  response['review'] != "":
            movie_to_update.review = response['review']
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/delete/<id>')
def delete(id):
    movie_to_delete = Movies.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method =="GET":
        add_form = AddForm(meta={'csrf': False})
        return render_template('add.html', form=add_form)
    else:
        movie_requested = request.form.to_dict()['movie_title']
        parameters = {
            'language': 'en-US',
            'query': movie_requested,
            'api_key': MOVIE_API_KEY,
            'page': 1

        }
        response = requests.get(API_ENDPOINT, params=parameters)
        results = response.json()['results']

        return render_template('select.html', results=results)

@app.route('/selected/<id>')
def add_movie(id):
    parameters2={
        'movie_id': id,
        'api_key': MOVIE_API_KEY,
    }

    response = requests.get(f"{ENDPOINT_2}/{id}", params=parameters2)
    response = response.json()
    new_movie = Movies(title=response['original_title'],
                       img_url=f"https://image.tmdb.org/t/p/w500{response['poster_path']}",
                       year=response['release_date'],
                       description=response['overview'],
                       # rating= 7.8,
                       # ranking=10,
                       # review="To be Determined"
                       )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
