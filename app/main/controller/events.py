from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from ..service.mensaje_service import save_new_mensaje


@socketio.on('JOINED', namespace = '/mychat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    #room = session.get('room')
    room = message["room"]
    join_room(room)
    print("joined", room)
    emit('STATUS', room=room)


@socketio.on('SEND_MESSAGE', namespace = '/mychat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = message["room"]
    print(room, message)
    print("AAAAAAAAAAAAAAAAAAAAAA")
    mensaje = {
        'usuario': message["usuario"],
        'texto': message["texto"],
        'conversacion': message["conversacion"]
    }
    save_new_mensaje(data=mensaje)
    emit('MESSAGE', message, room=room)


@socketio.on('LEFT', namespace='/mychat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = message["room"]
    leave_room(room)
    print("leaved", room)
    emit('STATUS', room=room)

@socketio.on('mensaje', namespace='/mychat')
def func(mensaje):
    print(mensaje)
    emit('mensaje')
