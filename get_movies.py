
import json
import requests

def fetch_movie_data():
    all_movies = []
    for page in range(1, 101):  # 1페이지부터 100페이지까지
        url = f"https://api.themoviedb.org/3/movie/{1}?language=ko-KR"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2M2Q2MjEwYTM0ZTNiNTdiYWIyNjYyODdhN2VmOWM2MyIsInN1YiI6IjY2Mjc1NjE4Y2I2ZGI1MDE0OWFkZTJmMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.u1lmXXsBgTz0TuyQZx4nnO25pj1BeBu5sm8f_CBM6ZI"  # 여기에 본인의 API 키를 입력하세요
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'results' in data:
            all_movies.extend(data['results'])
        else:
            print(f"No movie data found in response for page {page}")
    return all_movies

def save_data_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    all_movies = fetch_movie_data()
    save_data_to_json(all_movies, 'all_movies.json')
    print('All movie data saved to all_movies.json')

if __name__ == '__main__':
    main()
