# ✅ MONKEY PATCH FIRST!
import eventlet

eventlet.monkey_patch()

# ✅ THEN import everything else
from flask import Flask
from flask_socketio import SocketIO, emit
from flask import request  # Add this import
import random
import socket

def get_local_ip():
    try:
        # This tricks the OS into telling us the default outbound IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "UNKNOWN"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

players = {}

@socketio.on('connect')
def on_connect():
    print('New client connected')


@socketio.on('join')
def on_join(data):
    player_id = data['id']
    players[player_id] = {
        'x': 0,
        'y': 0,
        'z': 0,
        'sid': request.sid,  # 🟢 Store this to match later # type: ignore
        'name':str(random.randint(1,1000))
    }
    print(f"Player {player_id} joined with sid {request.sid}") # type: ignore
    emit('update', players, broadcast=True)


@socketio.on('move')
def on_move(data):
    player_id = data['id']
    x = data['x']
    y = data['y']
    z = data['z']
    def setprop(prop, value):
        players[data["id"]][prop] = value
    #players[player_id]['x'] -= 5
    if player_id in players:
        if data["id"] == player_id:
            setprop("x", x)
            setprop("y", y)
            setprop("z", z)
            print(players[data["id"]])
    
    emit('update', players, broadcast=True)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid # type: ignore
    disconnected_id = None

    # Find player ID by matching sid
    for player_id, info in players.items():
        if info.get('sid') == sid:
            disconnected_id = player_id
            break

    if disconnected_id:
        print(f"Player {disconnected_id} disconnected")
        del players[disconnected_id]
        emit('update', players, broadcast=True)
    else:
        print(f"Unknown SID {sid} disconnected (not in player list)")

if __name__ == '__main__':
    print("Server running at:")
    print("  -> http://127.0.0.1:8000")
    print("  -> http://localhost:8000")
    print(f"  -> LAN: http://{get_local_ip()}:8000")
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
