from flask import Flask, redirect
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return redirect("https://breq.dev/apps/cards/")


if __name__ == "__main__":
    app.run()
