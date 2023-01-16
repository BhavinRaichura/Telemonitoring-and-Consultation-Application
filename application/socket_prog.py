from flask import request,session
from flask_socketio import join_room, leave_room, emit, send,rooms

from application import socketio


messages =['welcome to msger app']

users={}
medicine ={}

@socketio.on('medicines',namespace='/medsock')
def medicines(medObj):
    print('called!!')
    print(type(medObj))
    print(medObj)
    emit('showMed',medObj,broadcast=True)


@socketio.on('message')
def handleMessage(msg):
    print ('msg : '+msg['msg']+"  sid : " + users[request.sid])
    #messages.append(msg)
    room = msg['room']
    emit('message',{'msg' :msg['msg'], 'sender': users[request.sid]},broadcast=True,to = room)

@socketio.on('newUser')
def handle_new_user(userInfo):
    print(userInfo)
    users[request.sid] = userInfo['username']
    room = userInfo['roomNumber']
    join_room(userInfo['roomNumber'])
    emit('message',{'msg':'new user join!', 'sender': users[request.sid]},to=room)


@socketio.on('privateChat')
def privateChat(target_data):
    print(target_data)
    print(type(target_data))
    for key, value in users.items():
        if value == target_data['target']:
            target = key
    emit('message',{'msg':target_data['msg'],'sender':users[request.sid]},room = target)


@socketio.on('join_arduino_room',namespace='/arduino_response')
def join_arduino_room(roomId):
    join_room(roomId)
    print("--------------------")
    print('user has join arduino room')
    print("--------------------")


@socketio.on('arduino_to_server',namespace='/arduino_response')
def arduino_to_server(arduino_data):
    print(arduino_data)
    emit('put_arduino',arduino_data,broadcast=True,to =arduino_data['roomId'])

'''
@socketio.on('connect')
def connect(datas):
    emit('user-connected',session.get('USER_ID'),broadcast = True, to=datas['ROOM_ID'])
    '''