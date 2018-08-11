from flask import Flask, request, url_for, render_template, jsonify, json, abort
from flask_pymongo import PyMongo

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
    else:
        tasks = tasks_db.find({})
        data = {}
        for task in tasks:
            data[task["id"]] = {
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "done": bool(task["done"])
            }
        return (jsonify(data))

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['GET'])
def get_task(task_id):
    data = {}
    tasks_db = mongo.db.tasks
    tasks = tasks_db.find({"id": task_id})
    if tasks.count() == 0:
        abort(500)
    data = {}
    for task in tasks:
        data[task["id"]] = {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "done": bool(task["done"])
        }
    return (jsonify(data))

@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def add_tasks():
    #id = request.json["id"]
    title = request.json["title"]
    description = request.json.get('description', '')
    done = bool(request.json["done"])
    tasks_db = mongo.db.tasks
    tasks_count = tasks_db.find({}).count();
    tasks_db.insert({
        "id": tasks_count + 1,
        "title": title,
        "description": description,
        "done": done
    })
    return jsonify({
        "id": tasks_count + 1,
        "title": title,
        "description": description,
        "done": done
    })

@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['PUT'])
def update_task(task_id):
    data = {}
    tasks_db = mongo.db.tasks
    task = tasks_db.find({"id": task_id})
    if task.count() == 0:
        abort(500)
    title = request.json.get("title", task[0]["title"])
    description = request.json.get('description', task[0]["description"])
    done = bool(request.json.get("done", task[0]["done"]))
    update_query = tasks_db.update_one(
        { "id": task_id},
        {
            '$set' : {
                "title": title,
                "description": description,
                "done": done
            }
        }
    )
    return ("Task with ID " + str(task_id) + " is successfully updated.")


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods = ['DELETE'])
def delete_task(task_id):
    data = {}
    tasks_db = mongo.db.tasks
    tasks_db.delete_one({"id": task_id})
    return ("Task with ID " + str(task_id) + " is successfully deleted.")


@app.errorhandler(404)
def not_found_error(e):
    return "URL doesn't exist"

@app.errorhandler(500)
def not_found_error(e):
    return "Task not found"

app.run(debug = True, port = 8080)