from flask import Blueprint
from flask import current_app
from main_app import create_app
from main_app import login_manager
from models import *
from forms import *
from utils import *

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
)
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from werkzeug.routing import BuildError
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from PIL import Image

app = create_app()


@login_manager.user_loader
def load_user(employee_id):
    return Employee.query.get(int(employee_id))

# ------------------------------- MAIN APP ROUTES -----------------------------

# Home
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def index():
    form = GetQuote()
    spares = Spares.query.order_by(Spares.id.desc()).all()

    if request.method == 'POST':
        name = form.name.data
        phone_number = form.phone_number.data
        email = form.email.data
        model = form.model.data
        branch = form.branch.data

        print(name,phone_number,email,model,branch)
            
        quote = Quotes(
            name=name,
            phone_number=phone_number,
            email=email,
            model=model,
            branch=branch
        )
    
        db.session.add(quote)
        db.session.commit()
        flash(f"Message Sent", "success")
        return redirect(url_for("index"))

    return render_template("index.html",title="Sound Kenya | Home",spares=spares,form=form)

@app.route("/dashboard", methods=("GET", "POST"), strict_slashes=False)
@login_required
def dashboard():
    return render_template("dashboard.html",title="Sound Kenya | Dashboard")

@app.route("/sales", methods=("GET", "POST"), strict_slashes=False)
@login_required
def sales():
    return render_template("sales.html",title="Sound Kenya | Sales")

@app.route("/purchases", methods=("GET", "POST"), strict_slashes=False)
@login_required
def purchases():
    return render_template("purchases.html",title="Sound Kenya | Purchases")

@app.route("/invoices", methods=("GET", "POST"), strict_slashes=False)
@login_required
def invoices():
    return render_template("invoices.html",title="Sound Kenya | Invoices")

@app.route("/quotes", methods=("GET", "POST"), strict_slashes=False)
@login_required
def quotes():
    quotes = Quotes.query.order_by(Quotes.id.desc()).all()

    return render_template("quotes.html",title="Sound Kenya | Dashboard",quotes=quotes)


@app.route("/spares", methods=("GET", "POST"), strict_slashes=False)
@login_required
def spares():
    spares = Spares.query.order_by(Spares.id.desc()).all()
    return render_template("spares.html",
    title="Sound Kenya | spares",
    spares=spares
    )

@app.route("/my_sales", methods=("GET", "POST"), strict_slashes=False)
@login_required
def my_spares():
    spares = Spares.query.order_by(Spares.id.desc()).all()
    return render_template("spares.html",
    title="Sound Kenya | spares",
    spares=spares
    )
@app.route("/<int:spare_id>/update",
    methods=("GET", "POST"),
    strict_slashes=False,
)
@login_required
def update_spare(spare_id):
    spare = Spares.query.filter_by(id=spare_id).first()

    form = AddSpare()
    if request.method=='POST':
   
        picture_file = upload_img(form.spare_img.data)

        spare.spare_img = picture_file
        spare.name = form.name.data
        spare.description = form.description.data

        db.session.commit()

        flash("Record succesfully Updated", "success")
        return redirect(url_for("spares"))

    elif request.method == "GET":
        form.spare_img.data = spare.spare_img
        form.name.data = spare.name
        form.description.data = spare.description

    return render_template("add.html",
        title="Sound Kenya | Update spare",
        form=form,
        button_text="Update Spare"
        )

@app.route("/<int:spare_id>/delete",
    methods=("GET", "POST"),
    strict_slashes=False,
)
@login_required
def delete_spare(spare_id):
    spare = Spares.query.filter_by(id=spare_id).first()

    flash("spare has been deleted succesfully ", "success")
    db.session.delete(spare)
    db.session.commit()
    return redirect(url_for("spares"))


@app.route("/add_spare", methods=("GET", "POST"), strict_slashes=False)
@login_required
def add():
    form= AddSpare()
    if form.spare_img.data:
        picture_file = upload_img(form.spare_img.data)
        name = form.name.data
        spare_img = picture_file
        description = form.description.data

        spare = Spares(
            name=name,
            spare_img=spare_img,
            description=description,
        )
        db.session.add(spare)
        db.session.commit()
        flash(f"Spare successfully added", "success")
        return redirect(url_for("spares"))

    return render_template("add.html",
        title="Sound Kenya | Add Spares",
        form=form,
        button_text="Add Spare"
        )

if __name__ == "__main__":
    app.run(debug=True)
