from http import client
from flask import Flask

from flask_socketio import SocketIO
from pymongo import MongoClient
from flask_restful import Resource, Api


app = Flask(__name__)

app.config['SECRET_KEY']= 'socketapp'
app.config['DEBUG']=True

socketio = SocketIO(app,cors_allowed_origins="*")

client = MongoClient("mongodb+srv://practicedb:practicedb@cluster0.73alj.mongodb.net/?retryWrites=true&w=majority")

db = client.telemed

api = Api(app)


from application import routes  
from application import socket_prog
from application import rest_API
from application import restAPIs