import requests
import json
import Movie

# The API key for The Movie Database (TMDb)
BEARER_TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2M2Q2MjEwYTM0ZTNiNTdiYWIyNjYyODdhN2VmOWM2MyIsInN1YiI6IjY2Mjc1NjE4Y2I2ZGI1MDE0OWFkZTJmMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.u1lmXXsBgTz0TuyQZx4nnO25pj1BeBu5sm8f_CBM6ZI'

# 원본 영화 정보가 저장된 JSON 파일 경로
json_file_path = 'all_movies.json'

# 수정된 영화 정보를 저장할 JSON 파일 경로
updated_json_file_path = 'update_movie.json'

# JSON 파일에서 영화 정보를 읽어오기
with open(json_file_path, 'r', encoding='utf-8') as file:
    movies_data = json.load(file)

# 각 영화에 대해 크레딧 정보를 가져와서 추가하기
for movie_data in movies_data:
    movie_id = movie_data['id']
    
    # TMDb API를 사용하여 영화의 크레딧 정보 가져오기
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko-KR"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    credits_data = response.json()
    
    # 배우 및 감독 정보 추출하기
    cast = credits_data.get('cast', [])
    crew = credits_data.get('crew', [])
    
    # 배우 이름 목록 (known_for_department가 "Acting"인 사람들만)
    actors = [member['name'] for member in cast if member['known_for_department'] == 'Acting']
    
    # 감독 이름 목록 (crew 중에서 job이 'Director'인 사람)
    directors = [member['name'] for member in crew if member['job'] == 'Director']
    
    # 기존 영화 데이터에 배우 및 감독 정보 추가하기
    movie_data['actors'] = actors
    movie_data['directors'] = directors
    
    
    
    
    

# 수정된 데이터를 새로운 JSON 파일에 저장하기
with open(updated_json_file_path, 'w', encoding='utf-8') as file:
    json.dump(movies_data, file, ensure_ascii=False, indent=4)

print("배우 및 감독 정보가 추가된 update_movie.json 파일이 저장되었습니다.")


