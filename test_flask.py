from flask import Flask, render_template, url_for
from test_forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "5217428b7b904e7c95b9a7e79f824704"

posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "April 20th 2018"
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 21st 2018"
    }
]


@app.route("/")
def hello():
    return render_template("test_home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("test_about.html", title="About")


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("test_register.html", title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("test_login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
