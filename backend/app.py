from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "miapp"),
        user=os.getenv("DB_USER", "usuario"),
        password=os.getenv("DB_PASSWORD", "secreto")
    )

# Crear tabla al iniciar
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id SERIAL PRIMARY KEY,
            texto TEXT NOT NULL,
            creado_en TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/api/mensajes", methods=["GET"])
def get_mensajes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, texto, creado_en FROM mensajes ORDER BY creado_en DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "texto": r[1], "fecha": str(r[2])} for r in rows])

@app.route("/api/mensajes", methods=["POST"])
def add_mensaje():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO mensajes (texto) VALUES (%s) RETURNING id", (data["texto"],))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "texto": data["texto"]}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
