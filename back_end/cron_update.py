import requests
from database import inserir_midia, create_tables
import os

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise RuntimeError("TMDB_API_KEY não definida")


BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/original"

CATEGORIAS = {
    "popular": f"{BASE_URL}/trending/movie/week?api_key={TMDB_API_KEY}&language=pt-BR",
    "movie": f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=pt-BR",
    "series": f"{BASE_URL}/tv/popular?api_key={TMDB_API_KEY}&language=pt-BR",
    "kids": f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres=16&language=pt-BR"
}

def get_trailer(tipo, tmdb_id):
    url = f"{BASE_URL}/{tipo}/{tmdb_id}/videos?api_key={TMDB_API_KEY}&language=pt-BR"
    res = requests.get(url).json()
    for v in res.get("results", []):
        if v["site"] == "YouTube" and v["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={v['key']}"
    return None

def get_details(tipo, tmdb_id):
    url = f"{BASE_URL}/{tipo}/{tmdb_id}?api_key={TMDB_API_KEY}&language=pt-BR"
    res = requests.get(url).json()
    return res

def processar_item(item, categoria, tipo):
    detalhes = get_details(tipo, item["id"])  # busca detalhes completos para pegar gêneros
    generos = detalhes.get("genres", [])
    generos_str = ", ".join([g['name'] for g in generos]) if generos else ""
    
    return {
        "id": item["id"],
        "type": tipo,
        "title": item.get("title") or item.get("name"),
        "overview": item.get("overview", ""),
        "poster": f"{IMG_URL}{item['poster_path']}" if item.get("poster_path") else "",
        "backdrop": f"{IMG_URL}{item['backdrop_path']}" if item.get("backdrop_path") else "",
        "rating": item.get("vote_average", 0),
        "trailer": get_trailer(tipo, item["id"]),
        "categoria": categoria,
        "generos": generos_str
    }

def atualizar():
    print("Atualizando banco de dados...")
    create_tables()

    for categoria, url in CATEGORIAS.items():
        tipo = "tv" if categoria == "series" else "movie"
        res = requests.get(url).json()
        itens = []

        for item in res.get("results", [])[:10]:
            dados = processar_item(item, categoria, tipo)
            itens.append(dados)

        inserir_midia(itens, categoria)
        print(f"✅ Atualizado: {categoria}")

    print("🎉 Finalizado!")

if __name__ == "__main__":
    atualizar()
