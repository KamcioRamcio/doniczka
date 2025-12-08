import sys
from pathlib import Path
from flask_app import Flask

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

app = Flask(__name__)

from routes.hat_sensor import hat_sensor_bp

app.register_blueprint(hat_sensor_bp)

if __name__ == "__main__":
    print("=" * 60)
    print("🌱 Inteligentna Doniczka - Multi-Sensor Dashboard")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
