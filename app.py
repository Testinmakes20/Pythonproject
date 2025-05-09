
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


# New API Routes

@app.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{"id": todo.id, "title": todo.title,
                     "complete": todo.complete}
                    for todo in todos])


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "Title is required"}), 400
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"id": new_todo.id, "title": new_todo.title,
                    "complete": new_todo.complete}), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json()
    title = data.get("title", todo.title)
    complete = data.get("complete", todo.complete)
    todo.title = title
    todo.complete = complete
    db.session.commit()
    return jsonify({"id": todo.id, "title": todo.title,
                    "complete": todo.complete})


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return '', 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
