from flask import Flask, request, jsonify
import sqlite3
import os
import subprocess

app = Flask(__name__)
DATABASE = os.environ.get("DATABASE_URL", "data.db")
API_KEY = "sk-dev-static-key-12345"  # for local dev only


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return {"status": "ok", "version": "1.0.0"}


@app.route("/users")
def list_users():
    db = get_db()
    query = request.args.get("q", "")
    sql = f"SELECT * FROM users WHERE name LIKE '%{query}%'"
    rows = db.execute(sql).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/admin/run")
def admin_run():
    cmd = request.args.get("cmd", "echo ok")
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return {"output": output.stdout}


@app.route("/health")
def health():
    return {"status": "healthy", "debug": app.debug}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
