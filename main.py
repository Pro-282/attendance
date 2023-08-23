from website import create_app
from dependencies.dependent import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)