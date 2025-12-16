from flask import Blueprint, render_template, jsonify, request
from flask import Blueprint, render_template, jsonify, request
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from hardware.actuators import Servo, Pump

control_bp = Blueprint('control', __name__)

servo_instance = None
pump_instance = None
current_angle = 0


def get_servo():
    """Get or initialize servo instance."""
    global servo_instance
    if servo_instance is None:
        servo_instance = Servo()
        servo_instance._pi_setup()
    return servo_instance


def get_pump():
    """Get or initialize pump instance."""
    global pump_instance
    if pump_instance is None:
        pump_instance = Pump()
    return pump_instance


@control_bp.route('/control')
def control_page():
    """Page for manual plant rotation control."""
    return render_template('control.html')


@control_bp.route('/api/control/rotate', methods=['POST'])
def rotate_plant():
    """API endpoint to rotate plant left or right."""
    global current_angle

    try:
        data = request.get_json()
        direction = data.get('direction', '')

        if direction not in ['left', 'right']:
            return jsonify({"error": "Invalid direction. Use 'left' or 'right'"}), 400

        servo = get_servo()
        new_angle = servo.user_rotate_plant(direction, current_angle)
        current_angle = new_angle

        return jsonify({
            "success": True,
            "current_angle": current_angle,
            "direction": direction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@control_bp.route('/api/control/angle', methods=['GET'])
def get_current_angle():
    """Get current servo angle."""
    global current_angle
    return jsonify({"current_angle": current_angle})


@control_bp.route('/api/control/reset', methods=['POST'])
def reset_position():
    """Reset servo to center position (0 degrees)."""
    global current_angle

    try:
        servo = get_servo()
        servo.set_servo_angle(0)
        current_angle = 0

        return jsonify({
            "success": True,
            "current_angle": current_angle
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@control_bp.route('/api/control/water', methods=['POST'])
def water_plant():
    """Water the plant for specified duration."""
    try:
        data = request.get_json()
        duration = data.get('duration', 1)

        if duration < 1 or duration > 2:
            duration = 1

        pump = get_pump()
        pump.user_water_plant(duration)

        return jsonify({
            "success": True,
            "duration": duration
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@control_bp.route('/api/control/stop-pump', methods=['POST'])
def stop_pump():
    """Emergency stop for the pump."""
    try:
        pump = get_pump()
        pump.stop_pump()

        return jsonify({
            "success": True,
            "message": "Pump stopped"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


