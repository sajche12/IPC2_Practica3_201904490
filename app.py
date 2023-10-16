from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

movies = [
    { "movieId": 1, "name": "The Shawshank Redemption", "genre": "Drama" },
    { "movieId": 2, "name": "The Godfather", "genre": "Drama" },
    { "movieId": 3, "name": "The Dark Knight", "genre": "Action" },
    { "movieId": 4, "name": "12 Angry Men", "genre": "Drama" },
    { "movieId": 5, "name": "Schindler's List", "genre": "Biography" }]

@app.route('/')
def home():
    return '<h1> Welcome to Movie Store! </h1>'

@app.route('/new-movie', methods=['POST'])
def add_movie():
    data = request.get_json()

    movie_id = data.get('movieId')
    name = data.get('name')
    genre = data.get('genre')
    if movie_id is None or name is None or genre is None:
        return jsonify({'message': 'Todos los campos son requeridos'}), 400

    # Verifica si la película ya existe
    existing_movie = next((movie for movie in movies if movie['movieId'] == movie_id), None)

    if existing_movie:
        return jsonify({'message': 'La película ya existe'}), 400

    # Agrega la nueva película a la base de datos simulada
    movies.append({'movieId': movie_id, 'name': name, 'genre': genre})

    return jsonify({'message': f'Película "{name}" agregada con éxito'}), 201

@app.route('/all-movies-by-genre/<genre>', methods=['GET'])
def get_movies_by_genre(genre):
    genre_movies = []
    for movie in movies:
        if movie['genre'] == genre:
            genre_movies.append(movie)
    return jsonify(genre_movies)

@app.route('/update-movie', methods=['PUT'])
def update_movie():
    movie = request.json
    for m in movies:
        if m['movieId'] == movie['movieId']:
            m['name'] = movie['name']
            m['genre'] = movie['genre']
            return jsonify({'message': 'Movie updated successfully'}), 200
    return jsonify({'message': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)