import json

def convert_to_django_model(movie_data_list):
    converted_movies = []
    for movie_data in movie_data_list:
        converted_movie = {
            "model": "yourapp.movie",
            "pk": movie_data["id"],
            "fields": {
                "title": movie_data["title"],
                "overview": movie_data["overview"],
                "poster_path": movie_data["poster_path"],
                "release_date": movie_data["release_date"],
                "vote_average": movie_data["vote_average"],
                "actors": movie_data["actors"],
                "directors": movie_data["directors"],
                "genre_ids": movie_data["genre_ids"]
            }
        }
        converted_movies.append(converted_movie)
    return converted_movies

# update_movies.json 파일에서 데이터를 읽어옵니다.
with open('update_movies.json', 'r', encoding='utf-8') as file:
    movie_data_list = json.load(file)

# 변환된 데이터 출력
converted_movies = convert_to_django_model(movie_data_list)
print(json.dumps(converted_movies, indent=4))
