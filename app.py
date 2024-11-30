from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Define and initialize the base model
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Define table schema
class Tasks(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str]

# Initialize the Flask app
app = Flask(__name__)

# Configure the SQLiteCloud database (connection)
# Requires a 'config.py' file with the sqlitecloud connection string as SQLALCHEMY_DATABASE_URI
app.config.from_pyfile('config.py')

# Initialize the app with the SQLAlchemy extension
db.init_app(app)

# Create the table(s)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # Query and return ALL tasks
    tasks = Tasks.query.all()
    return render_template('index.html', tasks=tasks)


@app.route("/create", methods=['POST',])
def create():
    # Add a new task, query and return new list of ALL tasks
    task = Tasks(task=request.form["task"],)
    db.session.add(task)
    db.session.commit()

    tasks = Tasks.query.all()

    return render_template('generate_task_list.html', tasks=tasks)

@app.route("/delete/<int:task_id>", methods=['POST',])
def delete(task_id):
    # Delete a task, query and return new list of ALL tasks
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    tasks = Tasks.query.all()

    return render_template('generate_task_list.html', tasks=tasks)
