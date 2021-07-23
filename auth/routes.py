from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from .forms import *
from . import *
from wtforms import ValidationError, validators
from main_app import db, bcrypt, login_manager
from flask import current_app
from flask_login import (
    UserMixin,
    login_required,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    send_from_directory,
)
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from utils import *
from flask_bcrypt import generate_password_hash, check_password_hash
from models import *


auth = Blueprint("auth", __name__, url_prefix="/0")


@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))  


# lOGIN route
@auth.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = Employee.query.filter_by(uname=form.uname.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Username or password!", "danger")
        except:
            flash("Invalid Username or password!", "danger")

    return render_template("auth.html",
        form=form,
        legend="Login",
        title="Sound Kenya | Login",
        action="Login"
        )



# Register route
@auth.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            pwd = form.pwd.data
            uname = form.uname.data
            lname = form.lname.data
            fname = form.fname.data
            
            newemployee = Employee(
                uname=uname,
                lname=lname,
                fname=fname,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newemployee)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("auth.login"))
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

            
    return render_template("auth.html",
        form=form,
        legend="Create account",
        title="Sound Kenya | Register",
        action="Register account"
        )

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

