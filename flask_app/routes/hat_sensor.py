from flask_app import Blueprint, render_template, jsonify
import sqlite3
import pandas as pd
from pathlib import Path

hat_sensor_bp = Blueprint('hat_sensor', __name__)


def get_sensor_data(limit=40):
    """
    Pobiera ostatnie pomiary WSZYSTKICH czujników z bazy danych.

    Args:
        limit (int): Liczba ostatnich pomiarów

    Returns:
        pd.DataFrame: DataFrame z kolumnami: id, temperature, pressure, humidity, light, uv
    """
    conn = None
    try:
        # Ścieżka do bazy danych
        project_root = Path(__file__).resolve().parent.parent
        db_path = "database/doniczka.db"

        conn = sqlite3.connect(str(db_path))

        # Pobierz wszystkie kolumny czujników
        query = f"""
            SELECT id, temperature, pressure, humidity, light, uv
            FROM env_sensor 
            ORDER BY id DESC 
            LIMIT {limit}
        """

        df = pd.read_sql_query(query, conn)

        # Odwróć kolejność (najstarsze na początku)
        df = df.iloc[::-1].reset_index(drop=True)

        return df

    except sqlite3.Error as e:
        print(f"❌ Błąd bazy danych: {e}")
        return pd.DataFrame(columns=['id', 'temperature', 'pressure', 'humidity', 'light', 'uv'])

    finally:
        if conn:
            conn.close()


@hat_sensor_bp.route('/')
def index():
    """Strona główna - Dashboard z 5 wykresami"""
    print("📊 Dashboard HAT - route accessed")
    return render_template('dashboard.html')


@hat_sensor_bp.route('/api/sensors/all')
def get_all_sensors():
    """
    API endpoint zwracający WSZYSTKIE dane czujników.

    Returns:
        JSON: {
            "temperature": [{x: id, y: temp}, ...],
            "pressure": [{x: id, y: press}, ...],
            "humidity": [{x: id, y: hum}, ...],
            "light": [{x: id, y: lux}, ...],
            "uv": [{x: id, y: uv}, ...]
        }
    """
    try:
        df = get_sensor_data(limit=40)

        if df.empty:
            print("⚠️  Brak danych w bazie")
            return jsonify({
                "temperature": [],
                "pressure": [],
                "humidity": [],
                "light": [],
                "uv": []
            })

        # Konwertuj każdą kolumnę na osobny dataset
        response = {
            "temperature": [
                {"x": int(row['id']), "y": float(row['temperature']) if pd.notna(row['temperature']) else None}
                for _, row in df.iterrows()
            ],
            "pressure": [
                {"x": int(row['id']), "y": float(row['pressure']) if pd.notna(row['pressure']) else None}
                for _, row in df.iterrows()
            ],
            "humidity": [
                {"x": int(row['id']), "y": float(row['humidity']) if pd.notna(row['humidity']) else None}
                for _, row in df.iterrows()
            ],
            "light": [
                {"x": int(row['id']), "y": float(row['light']) if pd.notna(row['light']) else None}
                for _, row in df.iterrows()
            ],
            "uv": [
                {"x": int(row['id']), "y": float(row['uv']) if pd.notna(row['uv']) else None}
                for _, row in df.iterrows()
            ]
        }

        print(f"✅ Zwrócono dane dla {len(df)} pomiarów (5 czujników)")
        return jsonify(response)

    except Exception as e:
        print(f"❌ Błąd w /api/sensors/all: {e}")
        return jsonify({"error": str(e)}), 500


@hat_sensor_bp.route('/api/stats')
def get_stats():
    """
    API endpoint ze statystykami dla wszystkich czujników
    """
    try:
        df = get_sensor_data(limit=100)

        if df.empty:
            return jsonify({"error": "Brak danych"})

        stats = {
            "temperature": {
                "current": float(df['temperature'].iloc[-1]) if not df.empty else None,
                "avg": float(df['temperature'].mean()),
                "min": float(df['temperature'].min()),
                "max": float(df['temperature'].max())
            },
            "pressure": {
                "current": float(df['pressure'].iloc[-1]) if not df.empty else None,
                "avg": float(df['pressure'].mean()),
                "min": float(df['pressure'].min()),
                "max": float(df['pressure'].max())
            },
            "humidity": {
                "current": float(df['humidity'].iloc[-1]) if not df.empty else None,
                "avg": float(df['humidity'].mean()),
                "min": float(df['humidity'].min()),
                "max": float(df['humidity'].max())
            },
            "light": {
                "current": float(df['light'].iloc[-1]) if not df.empty else None,
                "avg": float(df['light'].mean()),
                "min": float(df['light'].min()),
                "max": float(df['light'].max())
            },
            "uv": {
                "current": float(df['uv'].iloc[-1]) if not df.empty else None,
                "avg": float(df['uv'].mean()),
                "min": float(df['uv'].min()),
                "max": float(df['uv'].max())
            }
        }

        return jsonify(stats)

    except Exception as e:
        print(f"❌ Błąd w /api/stats: {e}")
        return jsonify({"error": str(e)}), 500
