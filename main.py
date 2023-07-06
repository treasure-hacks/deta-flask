import os
import sys
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


@app.route("/", methods=["GET", "POST"])
def index():
    """Home Page"""

    return render_template("index.html", todos=todos.fetch().items)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.form.get("name") and request.form.get("desc"):
        try:
            todos.put({"desc": request.form.get("desc")}, request.form.get("name"))
        except:
            return 500
        return redirect("/")
    else:
        return 400


@app.route("/delete", methods=["GET"])
def delete():
    try:
        todos.delete(request.args.get("todo"))
        return redirect("/")
    except:
        return 500

flags = [a for a in sys.argv[1:] if a.startswith('--')]
if __name__ == '__main__' and '--dev' in flags:
    # Run the app using Flask server in development only
    app.run(port = os.environ.get('PORT', 5000))
