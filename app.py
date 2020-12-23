import os
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


@app.route("/card")
@cross_origin()
def card():
    format = request.args.get("format")
    template_name = request.args.get("template")

    if not os.path.exists(f"templates/cards/{template_name}.html"):
        return abort(404)
    template = f"cards/{template_name}.html"

    if format == "html":
        args = {name: markdown(value)
                for name, value in request.args.items()}
        return render_template(template, **args)
    else:
        return abort(400)


if __name__ == "__main__":
    app.run()
