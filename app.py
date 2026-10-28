from flask import Flask, request
from models import db, Task, Employee

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
#======
def find_employee(employee_id):
    employee = Employee.query.get(employee_id)
    return employee
def find_task(task_id, employee_id=None):
    if employee_id is not None:
        employee = find_employee(employee_id)
        if not employee:
            return None
        task = Task.query.filter_by(id=task_id, employee_id=employee_id).first()
        return task
    return Task.query.get(task_id)
#======

@app.route('/')
def home():
    return "API работает, база данных подключена!"

#GET МАРШРУТЫ EMPLOYEES

@app.route('/employees')
def get_employees():
    employees = Employee.query.all()
    return {"employees": [t.to_dict() for t in employees]}

@app.route('/employees/<int:employee_id>/')
def find_employees(employee_id):
    employee = find_employee(employee_id)
    if employee is None:
        return {"error": "Сотрудник не найден"}, 404
    return employee.to_dict(), 200

@app.route('/employees/<int:employee_id>/tasks')
def get_employee_task(employee_id):
    tasks = Task.query.filter_by(employee_id=employee_id).all()
    return {"tasks": [t.to_dict() for t in tasks]}, 200

@app.route('/employees/<int:employee_id>/tasks/<int:task_id>')
def find_tasks(employee_id, task_id):   
    task = find_task(task_id=task_id, employee_id=employee_id)
    if not task:
        return {"error":"Задача не найдена"}
    return task.to_dict(), 200

#GET МАРШРУТЫ /TASKS

@app.route('/tasks')
def get_all_tasks():
    tasks = Task.query.all()
    return {"tasks": [t.to_dict() for t in tasks]}

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = find_task(task_id)
    if task is None:
        return {"error": "Задача не найдена"}, 404
    return task.to_dict(), 200

#POST МАРШРУТЫ EMPLOYEES

@app.route('/employees', methods=['POST'])
def create_employee():
    data =  request.get_json()
    new_employee = Employee(name=data.get('name'), role=data.get('role', 'unknown'))
    db.session.add(new_employee)
    db.session.commit()
    return new_employee.to_dict(), 201

#POST МАРШРУТЫ TASKS

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    emp_id = data.get('employee_id')
    if not emp_id:
        return {"error": "Поле 'employee_id' обязательно для заполнения!"}, 400
    employee_exists = Employee.query.get(emp_id)
    if not employee_exists:
        return {"error": f"Сотрудника с {emp_id} не существует"}, 404
    new_task = Task(title=data.get('title'), priority=data.get('priority'), employee_id=emp_id)
    db.session.add(new_task)
    db.session.commit()
    return new_task.to_dict(), 201
#PATCH МАРШРУТЫ
@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def task_patch(task_id):
    task = find_task(task_id)
    if task is None:
        return {"error": "Задача не найдена"}, 404
    data = request.get_json()
    if "done" in data:
        task.done = data["done"]
    db.session.commit()
    return task.to_dict(), 200
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = find_task(task_id)
    if task is None:
        return {"error": "Задача не найдена"}, 404
    db.session.delete(task)
    db.session.commit()
    return {"message": f"Задача {task_id} успешно удалена"}, 200
if __name__ == '__main__':
    app.run(debug=True)
