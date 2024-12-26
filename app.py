from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDoList.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False       # Used for 'Signal Emitting'
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    Sr_no = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now())
    
    def __repr__(self) -> str:
        return f"{self.Sr_no} - {self.title}"
    
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo = allTodo)      

@app.route('/update/<int:Sr_no>', methods = ['GET', 'POST'])
def update(Sr_no):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(Sr_no = Sr_no).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = Todo.query.filter_by(Sr_no=Sr_no).first()
    allTodo = Todo.query.all()
    return render_template('update.html', todo = todo)    

@app.route('/delete/<int:Sr_no>')
def delete(Sr_no):
    todo = Todo.query.filter_by(Sr_no = Sr_no).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/') 

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "ToDo List"
    
if __name__ == "__main__":
    app.run(debug = True, port = 17000)