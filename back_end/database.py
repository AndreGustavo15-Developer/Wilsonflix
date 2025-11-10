import sqlite3, os

DB_PATH = "database/wilsonflix.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS midia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER,
            tipo TEXT,
            categoria TEXT,
            titulo TEXT,
            descricao TEXT,
            poster TEXT,
            backdrop TEXT,
            nota REAL,
            trailer TEXT,
            generos TEXT,
            data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def inserir_midia(data_list, categoria):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # Remove o que já existe da categoria
    cur.execute("DELETE FROM midia WHERE categoria = ?", (categoria,))

    for item in data_list:
        generos_str = item.get("generos", "")

        cur.execute("""
            INSERT INTO midia (tmdb_id, tipo, categoria, titulo, descricao, poster, backdrop, nota, trailer, generos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.get("id"),
            item.get("type"),
            categoria,
            item.get("title"),
            item.get("overview"),
            item.get("poster"),
            item.get("backdrop"),
            item.get("rating"),
            item.get("trailer"),
            generos_str
        ))

    conn.commit()
    conn.close()


def buscar_por_categoria(categoria):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("SELECT * FROM midia WHERE categoria = ?", (categoria,))
    rows = cur.fetchall()
    conn.close()
    return rows

def buscar_por_id(tmdb_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute("SELECT * FROM midia WHERE tmdb_id = ?", (tmdb_id,))
    row = cur.fetchone()
    conn.close()
    return row
