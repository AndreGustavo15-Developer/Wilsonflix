from flask import Flask, jsonify
from flask_cors import CORS
from database import buscar_por_categoria, buscar_por_id, create_tables

app = Flask(__name__)
CORS(app, origins=["https://andregustavo15-developer.github.io"])

create_tables()

@app.route("/api/<categoria>")
def lista_por_categoria(categoria):
    rows = buscar_por_categoria(categoria)
    response = []

    for r in rows:
        response.append({
            "id": r["tmdb_id"],
            "type": r["tipo"],
            "categoria": r["categoria"],
            "title": r["titulo"],
            "overview": r["descricao"],
            "poster": r["poster"],
            "backdrop": r["backdrop"],
            "rating": r["nota"],
            "trailer": r["trailer"],
            "genres": r.get("generos", "")
        })

    return jsonify(response)

@app.route("/api/details/<int:tmdb_id>")
def detalhes(tmdb_id):
    r = buscar_por_id(tmdb_id)
    if not r:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": r["tmdb_id"],
        "type": r["tipo"],
        "categoria": r["categoria"],
        "title": r["titulo"],
        "overview": r["descricao"],
        "poster": r["poster"],
        "backdrop": r["backdrop"],
        "rating": r["nota"],
        "trailer": r["trailer"],
        "genres": r.get("generos", "")
    })


@app.route("/api/categorias")
def listar_categorias():
    import sqlite3
    conn = sqlite3.connect("database/wilsonflix.db")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT categoria FROM midia")
    resultado = [r[0] for r in cur.fetchall()]
    conn.close()
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
