import pytest
from models import Employee, Task, db
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all() 
        yield client       
        with app.app_context():
            db.drop_all()

# тест создания сотрудника

def test_create_employee(client):
    response = client.post('/employees', json={'name':'Бублик', 'role':'Водитель'})
    assert response.status_code == 201

# тест создания задачи с привязкой к существующему сотруднику;

def test_create_task(client):
    emp_res = client.post('/employees', json={'name':'Бублик', 'role':'Водитель'})
    emp_id = emp_res.get_json()['id']
    response = client.post('/tasks', json={'title':'Очистить сад', 'employee_id': emp_id})
    assert response.get_json()["priority"] == 3
    assert response.status_code == 201

# тест создания задачи с несуществующим employee_id — ожидается 404

def test_create_task_wtht_emp(client):
    response = client.post('/tasks', json={'title':'Очистить сад', 'employee_id': 99})
    assert response.status_code == 404

# тест создания задачи с неверным приоритетом — ожидается 400;

def test_wrong_priority_task(client):
    emp_res = client.post('/employees', json={'name':'Бублик', 'role':'Водитель'})
    emp_id = emp_res.get_json()['id']
    response = client.post('/tasks', json={'title' : 'Помыть посуду', 'priority': 6, 'employee_id': emp_id})
    assert response.status_code == 400 

# тест полного сценария: создать сотрудника → создать для него задачу

def test_ful_scenary(client):

    emp_response = client.post('/employees', json={'name':'Морбид', 'role':'Танкист'})
    assert emp_response.status_code == 201
    emp_id = emp_response.get_json()['id']  

    task_response = client.post('/tasks', json={'title':'Посадить дерево', 'employee_id': emp_id})
    assert task_response.status_code == 201
    task_id = task_response.get_json()['id']
   
    patch_response = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert patch_response.status_code == 200

    get_tasks_response = client.get(f"/employees/{emp_id}/tasks")
    assert get_tasks_response.status_code == 200
    
    tasks_list = get_tasks_response.get_json()["tasks"]
    assert len(tasks_list) == 1
    assert tasks_list[0]["done"] is True  
