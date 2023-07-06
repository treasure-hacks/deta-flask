from flask import Flask, redirect, render_template, request
from deta import Base

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

todos = Base("todos")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods = ["GET", "POST"])
def index():
    """Home Page"""

    return render_template("index.html", todos=todos.fetch().items)


@app.route('/todos', methods = ['GET'])
def get_tasks():
    tasks = todos.fetch().items
    return tasks


@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.json.get("name") and request.json.get("desc"):
        try:
            item = todos.put({"desc": request.json.get("desc")}, request.json.get("name"))
            return item
        except:
            return 500
    else:
        return 400


@app.route("/edit", methods = ["POST"])
def edit():
    name = request.json.get("name")
    desc = request.json.get("desc")
    old = request.json.get("old_key")
    if name and desc:
        try:
            if name != old: todos.delete(old)
            return todos.put({"key": name, "desc": desc})
        except:
            return 500
    else:
        return 400


@app.route("/delete", methods=["GET"])
def delete():
    try:
        todos.delete(request.args.get("todo"))
        return redirect("/")
    except:
        return 500
