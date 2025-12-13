
import config
if config.multiplayer:
    import socketio
    import uuid
    client = socketio.Client()
    id = str(uuid.uuid4())
    players = {}
    @client.event
    def connect():
        print('Connected to server')
        client.emit('join', {'id': id})

    @client.on('update') # type: ignore
    def on_update(data):
        global players
        players = data

    connectoserver = client.connect

    def move(x, y, z):
        client.emit("move", {"id": id, "x": str(x), "y": str(y), "z": str(z),})
