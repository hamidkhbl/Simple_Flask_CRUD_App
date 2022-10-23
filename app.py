from crypt import methods
from distutils.log import error
from flask import jsonify, redirect, abort
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoapp2'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    def __init__(self, desc):
        self.desctiption = desc
    id = db.Column(db.Integer, primary_key = True)
    desctiption = db.Column(db.String(50), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default=False)

def __repr__(self):
    return f'<Todo {self.id} {self.description}>'


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.order_by('id').all())

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    error = False
    body = {}
    description = request.get_json()['description']
    try:
        todo = Todo(description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.desctiption
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = True
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))
