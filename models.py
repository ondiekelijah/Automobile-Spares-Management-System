from main_app import db ,migrate,login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import event
from flask import current_app
import os


class Customer(UserMixin, db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(72), nullable=False)
    lname = db.Column(db.String(72), nullable=False)

class Employee(UserMixin, db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(72), nullable=False)
    lname = db.Column(db.String(72), nullable=False)
    pwd = db.Column(db.String(72), nullable=False, unique=True)
    uname = db.Column(db.String(20), nullable=False)
        
@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))  

class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser

class Spares(db.Model):
    __tablename__ = "spares"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spare_img = db.Column(db.String(150), default="no-image.jpg")
    description = db.Column(db.String(150))

    def __repr__(self):
        return "<Spares %r>" % self.name

class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spare_img = db.Column(db.String(150), default="no-image.jpg")
    description = db.Column(db.String(150))

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship("Customer", backref=db.backref("customer"), lazy=True)

    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    employee = db.relationship("Employee", backref=db.backref("employee"), lazy=True)

    def __repr__(self):
        return "<Sales %r>" % self.name


class Quotes(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(150), nullable=False)
    model = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return "<Sales %r>" % self.name