import os
import re
import asyncio

from quart import (Quart, request, redirect, render_template, abort, Markup,
                   Response)
from quart_cors import cors, route_cors

from pyppeteer import launch


app = Quart(__name__)
app = cors(app)


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


async def screenshot(html, type="png"):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({"width": 500, "height": 300})
    await page.setContent(html)
    await asyncio.sleep(1)
    image = await page.screenshot(type=type, omitBackground=True)
    await browser.close()
    return image


@app.route("/")
async def index():
    return redirect("https://breq.dev/apps/cards/")


@app.route("/card")
@route_cors(allow_origin="*")
async def card():
    format = request.args.get("format")
    template_name = request.args.get("template")

    if not os.path.exists(f"templates/cards/{template_name}.html"):
        return abort(404)
    template = f"cards/{template_name}.html"

    args = {name: markdown(value)
            for name, value in request.args.items()}

    if format == "html":
        return await render_template(template, **args)
    elif format == "png":
        html = await render_template(template, no_rounding=True, **args)
        image = await screenshot(html, "png")
        return Response(image, mimetype="image/png")
    elif format in ["jpg", "jpeg"]:
        html = await render_template(template, no_rounding=True, **args)
        image = await screenshot(html, "jpeg")
        return Response(image, mimetype="image/jpeg")
    else:
        return abort(400)


if __name__ == "__main__":
    app.run()
