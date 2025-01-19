from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import requests
import json

app_weather = Flask(__name__)

API_KEY = "faa7763d74msh5b00b30e485780dp1f058fjsnf655e6f127aa"
API_URL = "https://weatherapi-com.p.rapidapi.com/current.json"
API_HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
}

def get_db_connection():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn

def get_weather_data(city):
    querystring = {"q": city}
    response = requests.get(API_URL, headers=API_HEADERS, params=querystring)
    return response.json()

@app_weather.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    city = None
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather_data(city)

        if 'error' in weather_data:
            return render_template("index.html", error="Город не найден!")

        conn = get_db_connection()
        conn.execute("INSERT INTO search_history (city_name) VALUES (?)", (city,))
        conn.execute(
            "INSERT INTO saved_forecasts (city_name, forecast_data) VALUES (?, ?)",
            (city, json.dumps(weather_data)),
        )
        conn.commit()
        conn.close()

    conn = get_db_connection()
    history = conn.execute("SELECT * FROM search_history ORDER BY timestamp DESC LIMIT 5").fetchall()
    conn.close()

    return render_template("index.html", weather=weather_data, city=city, history=history)

@app_weather.route("/weather/<city_name>", methods=["GET"])
def city_weather(city_name):
    conn = get_db_connection()
    forecast = conn.execute(
        "SELECT forecast_data FROM saved_forecasts WHERE city_name = ? ORDER BY timestamp DESC LIMIT 1",
        (city_name,)
    ).fetchone()
    conn.close()

    if not forecast:
        return render_template("index.html", error="Прогноз для этого города не найден!")

    forecast_data = json.loads(forecast["forecast_data"])
    return jsonify(forecast_data)  # Возвращаем данные как JSON

@app_weather.route("/clear_history", methods=["GET"])
def clear_history():
    conn = get_db_connection()
    conn.execute("DELETE FROM search_history")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app_weather.run(debug=True)
