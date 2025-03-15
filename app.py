from datetime import datetime
from flask import Flask, render_template, url_for, redirect,request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now())
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def get_tasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks = tasks)
    
@app.route('/task', methods = ["POST", "GET"])
def task(): 
    if request.method == 'POST':
        new_task = Todo(text = request.form['task'])
        # check if if the task is already present in the list or any duplicate of that
        task = Todo.query.filter_by(text = new_task.text).first()
        if task:
           # If task exists, re-render with error message
            tasks = Todo.query.order_by(Todo.date_created).all()
            return render_template('task.html', error_message="Task already exists", tasks=tasks)
        else:   
            new_task = Todo(text = request.form['task'])
            # add the new task to the database
            try:
                db.session.add(new_task)
                db.session.commit()
                 # Fetch all tasks including the new one
                tasks = Todo.query.order_by(Todo.date_created).all()
                return render_template('task.html', tasks=tasks, success_message="Task added successfully")
            except Exception as e:
                return f"There was an issue adding your task {new_task}. Please try again later.{e}"
    else:
        # fetch all tasks from the database and display them
        tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('task.html', tasks = tasks)


@app.route('/task/delete/<int:id>')
def delete_task(id):
    # fetch the task with the given id from the database
    task = Todo.query.get_or_404(id)
    try:
        # delete the task from the database
        db.session.delete(task)
        db.session.commit()
        return redirect('/task')
    except Exception as e:
        return f"There was an issue deleting your task {task}. Please try again later.{e}"
    
@app.route('/task/update/<int:id>', methods = ["POST", "GET"])
def update(id):
    # fetch the task with the given id from the database
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.text = request.form['content']
        task.complete = request.form.get('complete', False)
        try:
            db.session.commit()
            return redirect('/task')
        except Exception as e:
            return f"There was an issue updating your task {task}. Please try again later.{e}"
    else:
        return render_template('update.html', task = task)
    


@app.route('/task/toggle/<int:id>', methods=['POST'])
def toggle_task(id):
    try:
        task = Todo.query.get_or_404(id) 
        # Get JSON data from request
        data = request.get_json()
        print(data)
        # Update task completed status
        task.completed = data.get('completed', False)
        # Commit changes to database
        db.session.commit()
        
        return jsonify({
            'success': True,
            'id': task.id,
            'completed': task.completed
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html')

# run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)
