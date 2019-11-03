from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
