from flask import jsonify, redirect
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import request

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
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    description = request.get_json()['description']
    todo = Todo(description)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'description': todo.desctiption
    })

