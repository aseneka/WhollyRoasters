from forms import RegistrationForm
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            username = form.data["uname"]
            password = form.data["pword"]
            confirm = form.data["confirm"]
            message = f"Successfully registered {username}!"
        else:
            message = "Registration failed."

    return render_template("register.html", message=message, form=form)
