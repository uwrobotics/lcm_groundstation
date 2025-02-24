from flask import Flask, jsonify, request, send_from_directory
from threading import Lock

app = Flask(__name__, static_url_path='')
state_lock = Lock()

# Global state
gui_state = {
    "gps_origin": [43.4723, -80.5449],  # University of Waterloo approximate
    "gps_path": [],  # List of [lat, lng] points
    "joystick": {"x": 0, "y": 0},  # Normalized values between -1 and 1
    "status_bars": [0, 0, 0, 0, 0, 0, 0],  # 7 values in range [-100, 100]
    "gps_status": {"connected": 0, "status": "Disconnected"},
    "system_message": "System ready."
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/data', methods=['GET'])
def get_data():
    with state_lock:
        return jsonify(gui_state)

@app.route('/set', methods=['POST'])
def set_data():
    """
    Expects a JSON payload with any subset of:
    {
        "gps_path": [[lat, lng], ...],
        "joystick": {"x": float, "y": float},
        "status_bars": [int, int, ...],  // length 7
        "gps_status": {"connected": int, "status": str},
        "system_message": str
    }
    """
    data = request.get_json()
    with state_lock:
        for key in data:
            if key in gui_state:
                gui_state[key] = data[key]
    return jsonify({"result": "success", "new_state": gui_state})

if __name__ == '__main__':
    # Run the app (in debug mode for testing)
    app.run(host='0.0.0.0', port=5000, debug=True)
