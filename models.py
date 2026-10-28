from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="unknown")
    tasks = db.relationship("Task", backref="assignee", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "role": self.role}

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, default=3)
    done = db.Column(db.Boolean, default=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "priority": self.priority,
            "done": self.done, "employee_id": self.employee_id
        }