import time
from flask import Flask,render_template,session,request
from flask_socketio import SocketIO,emit,disconnect

app=Flask(__name__)
app.config["SECRET_KEY"]="SECRET_KEY"

count=0
item_target=None

socketio=SocketIO(app,async_mode=None)

@socketio.on('connect',namespace="/test")
def test_connect():
        emit('responce',{"data":'connected','count':count})


@socketio.on('sample_event',namespace="/test")
def test_responce(msg):
    print("msg",msg)
    global count
    while True:
        count+=1
        if count>50:
            count=0
        print(count)
        emit('responce',{"data":'responce','count':count})
        time.sleep(1)

@socketio.on('item_target')
def item_available(item_target):
    print(item_target)


@socketio.on('item_available')
def item_available(msg):
    print(msg)
    while True:
        emit('item_available',{})
        time.sleep(1)


socketio.run(app,host="0.0.0.0",port=80)



