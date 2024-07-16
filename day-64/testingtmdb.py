import requests
import json

movie_name = input("Movie name: ")

movie_name = movie_name.split(" ")
movie_name = "%20".join(movie_name)

url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"


headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYTk5MTIzNTUzZjFmZTRkODMxNmRlZWE3NDI1ZGY5NyIsIm5iZiI6MTcyMTA2MjIxOS40NDEzMSwic3ViIjoiNjY5NTJiZTk3ZDk5YmIxYjBjYTk3NDVmIiwic2NvcGVzIjpbImFwaV9yZWFkIl0sInZlcnNpb24iOjF9.3lITiSgys__fAV09n5n9NfNFAR6fFHjHAb9yJzgRAKM"
}

response = requests.get(url, headers=headers)
print(response)
response.raise_for_status()

results = response.json()
# with open("results.json", "w") as results_file:
#     json_string = json.dumps(results, indent=4)
#     results_file.write(json_string)
print(results["results"][0])
