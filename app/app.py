import os
import time
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("POSTGRES_DB", "portfolio_db"),
    "user": os.getenv("POSTGRES_USER", "portfolio_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "portfolio_pass"),
}


def connection(retries=20, delay=2):
    last_error = None
    for _ in range(retries):
        try:
            return psycopg2.connect(**DB)
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error


@app.get("/")
def index():
    return jsonify(
        service="docker-portfolio-api",
        endpoints=["GET /health", "GET /api/messages", "POST /api/messages"],
    )


@app.get("/health")
def health():
    try:
        with connection(retries=1) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return jsonify(status="healthy", database="connected"), 200
    except Exception:
        return jsonify(status="unhealthy", database="disconnected"), 503


@app.post("/api/messages")
def create_message():
    payload = request.get_json(silent=True) or {}
    content = str(payload.get("content", "")).strip()
    if not content:
        return jsonify(error="Field 'content' is required"), 400
    if len(content) > 500:
        return jsonify(error="Message is too long (max 500 characters)"), 400

    with connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO messages(content) VALUES (%s) RETURNING id, content, created_at",
                (content,),
            )
            row = cur.fetchone()
        conn.commit()
    return jsonify(row), 201


@app.get("/api/messages")
def list_messages():
    with connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT id, content, created_at FROM messages ORDER BY id DESC LIMIT 50"
            )
            rows = cur.fetchall()
    return jsonify(rows), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
