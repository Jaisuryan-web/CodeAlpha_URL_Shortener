from flask import Flask, request, redirect, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route("/")
def home():
    return """
    <h1>URL Shortener</h1>
    <p>Use the /shorten endpoint with POST request to shorten URLs</p>
    <p>Example: POST to /shorten with JSON: {"long_url": "https://example.com"}</p>
    """

# Generate short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# API to shorten URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("long_url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (long_url, short_code) VALUES (?, ?)",
        (long_url, short_code)
    )
    conn.commit()
    conn.close()

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

# Redirect route
@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT long_url FROM urls WHERE short_code = ?",
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
