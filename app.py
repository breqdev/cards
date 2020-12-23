import re

from flask import Flask, request, redirect, render_template, abort, Markup
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


def markdown(text):
    text = Markup.escape(text).unescape()
    text = re.sub("\n\n", "<br>", text)
    text = re.sub(
        r"\*\*(.*)\*\*", r" <strong>\1</strong> ", text, re.DOTALL)
    text = re.sub(
        r"\*(.*)\*", r" <em>\1</em> ", text, re.DOTALL)
    text = re.sub(
        r"`(.*)`", r" <code>\1</code> ", text, re.DOTALL)
    text = re.sub(
        r"\~\~(.*)\~\~", r" <strike>\1</strike> ", text, re.DOTALL)
    return Markup(text)


@app.route("/")
def index():
    return redirect("https://breq.dev/apps/cards/")


@app.route("/card/<string:template_name>", methods=["POST"])
@cross_origin()
def card(template_name):
    format = request.args.get("format")

    if format == "html":
        args = {name: markdown(value)
                for name, value in request.form.items()}
        return render_template("basic.html", **args)
    else:
        return abort(400)


if __name__ == "__main__":
    app.run()
