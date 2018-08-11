from flask import Flask, request, url_for, render_template, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pprint

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'todo_db'
app.config['MONGO_URI'] = 'mongodb://admin:admin123@ds219432.mlab.com:19432/todo_db'

mongo = PyMongo(app)

@app.route("/todo/api/v1.0/tasks", methods = ['GET'])
def index():
    data = {}
    tasks_db = mongo.db.tasks
    tasks_count = tasks_db.find({}).count();
    if (tasks_count == 0):
        data["tasks"] = str(tasks_count) + " tasks are found"
        return (jsonify(data))

@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def add_tasks():
    id = request.json["id"]
    title = request.json["title"]
    description = request.json.get('description', '')
    done = request.json["done"]
    tasks_db = mongo.db.tasks
    tasks_count = tasks_db.find({}).count();
    task_info = {
        "id": tasks_count + 1,
        "title": title,
        "description": description,
        "done": done
    }
    tasks_db.insert({
        "task": task_info
    })
    return jsonify({"task": task_info})


app.run(debug=True, port = 8080)