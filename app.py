from flask import Flask, request, url_for, render_template, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pprint

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'todo_db'
app.config['MONGO_URI'] = 'mongodb://admin:admin123@ds219432.mlab.com:19432/todo_db'

mongo = PyMongo(app)

@app.route("/")
def index():
    return "Hello World!"

app.run(debug=True, port = 8080)