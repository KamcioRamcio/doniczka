from flask import Blueprint, render_template, jsonify
import sqlite3
import pandas as pd
from pathlib import Path

hat_sensor_bp = Blueprint('hat_sensor', __name__)


def get_sensor_data(limit=40):
    """Pobiera ostatnie pomiary wszystkich czujników z bazy danych."""
    conn = None
    try:
        project_root = Path(__file__).resolve().parent.parent
        db_path = "database/doniczka.db"

        conn = sqlite3.connect(str(db_path))

        query = f"""
            SELECT e.id, e.temperature, e.pressure, e.humidity, e.light, e.uv, m.moisture, e.time_pnt
            FROM env_sensor e
            JOIN moist_sensor m ON e.id = m.id
            ORDER BY e.id DESC 
            LIMIT {limit}
        """

        df = pd.read_sql_query(query, conn)

        df = df.iloc[::-1].reset_index(drop=True)

        return df

    except sqlite3.Error as e:
        return pd.DataFrame(columns=['id', 'temperature', 'pressure', 'humidity', 'light', 'uv', 'moisture', 'time_pnt'])

    finally:
        if conn:
            conn.close()


@hat_sensor_bp.route('/')
def index():
    """Strona główna - Dashboard"""
    return render_template('dashboard.html')


@hat_sensor_bp.route('/api/sensors/all')
def get_all_sensors():
    """API endpoint zwracający wszystkie dane czujników."""
    try:
        df = get_sensor_data(limit=40)

        if df.empty:
            return jsonify({
                "temperature": [],
                "pressure": [],
                "humidity": [],
                "light": [],
                "uv": [],
                "moisture": [],
                "time_pnt": []
            })

        response = {
            "temperature": [
                {"x": row['time_pnt'], "y": float(row['temperature']) if pd.notna(row['temperature']) else None}
                for _, row in df.iterrows()
            ],
            "pressure": [
                {"x": row['time_pnt'], "y": float(row['pressure']) if pd.notna(row['pressure']) else None}
                for _, row in df.iterrows()
            ],
            "humidity": [
                {"x": row['time_pnt'], "y": float(row['humidity']) if pd.notna(row['humidity']) else None}
                for _, row in df.iterrows()
            ],
            "light": [
                {"x": row['time_pnt'], "y": float(row['light']) if pd.notna(row['light']) else None}
                for _, row in df.iterrows()
            ],
            "uv": [
                {"x": row['time_pnt'], "y": float(row['uv']) if pd.notna(row['uv']) else None}
                for _, row in df.iterrows()
            ],
            "moisture": [
                {"x": row['time_pnt'], "y": float(row['moisture']) if pd.notna(row['moisture']) else None}
                for _, row in df.iterrows()
            ]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@hat_sensor_bp.route('/api/stats')
def get_stats():
    """API endpoint ze statystykami dla wszystkich czujników."""
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
        return jsonify({"error": str(e)}), 500
