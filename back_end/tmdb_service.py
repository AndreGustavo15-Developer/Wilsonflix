import requests

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY não definida")

BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/original"

def fetch(endpoint):
    url = f"{BASE_URL}{endpoint}&api_key={TMDB_API_KEY}&language=pt-BR"
    return requests.get(url).json().get("results", [])[:10]


def get_trailer(tmdb_id, tipo):
    url = f"{BASE_URL}/{tipo}/{tmdb_id}/videos?api_key={TMDB_API_KEY}&language=pt-BR"
    videos = requests.get(url).json().get("results", [])

    for v in videos:
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            return f"https://www.youtube.com/embed/{v.get('key')}"
    return None


def format_item(data, tipo):
    trailer = get_trailer(data.get("id"), tipo)

    return {
        "id": data.get("id"),
        "type": tipo,
        "title": data.get("title") or data.get("name"),
        "overview": data.get("overview"),
        "rating": data.get("vote_average"),
        "poster": IMG_URL + data["poster_path"] if data.get("poster_path") else None,
        "backdrop": IMG_URL + data["backdrop_path"] if data.get("backdrop_path") else None,
        "trailer": trailer
    }

def get_popular_movies():
    return [format_item(f, "movie") for f in fetch("/movie/popular?")]

def get_movies():
    return [format_item(f, "movie") for f in fetch("/trending/movie/week?")]

def get_series():
    return [format_item(f, "tv") for f in fetch("/tv/popular?")]

def get_kids():
    return [format_item(f, "movie") for f in fetch("/discover/movie?certification_country=BR&certification.lte=L&")]
