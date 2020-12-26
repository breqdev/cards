import os
import re
import asyncio
import contextlib
import aiohttp

from quart import (Quart, request, redirect, render_template, abort, Markup,
                   Response, jsonify, send_file)
from quart_cors import cors, route_cors

from pyppeteer import launch

CHROME_PATH = os.environ.get('GOOGLE_CHROME_SHIM')
STORAGE_PATH = os.environ.get("STORAGE_PATH") or "./storage"


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


@contextlib.asynccontextmanager
async def open_html(html):
    browser = await launch(executablePath=CHROME_PATH)
    page = await browser.newPage()
    await page.setViewport({"width": 500, "height": 300})
    await page.setContent(html)
    await page.waitFor("*")
    await page.waitForFunction("isReady()")
    await asyncio.sleep(0.1)  # Font Awesome takes longer to load in
    try:
        yield page
    finally:
        await browser.close()


async def screenshot(html, **options):
    async with open_html(html) as page:
        image = await page.screenshot(**options)
    return image


@app.route("/")
async def index():
    return redirect("https://breq.dev/apps/cards/")


@app.route("/card", methods=["GET", "POST"])
@route_cors(allow_origin="*")
async def card():
    template_name = request.args.get("template")

    if not os.path.exists(f"templates/cards/{template_name}.html"):
        return abort(404)
    template = f"cards/{template_name}.html"

    args = {name: markdown(value)
            for name, value in request.args.items()}

    html = await render_template(template, **args)

    if request.method == "GET":
        format = request.args.get("format")

        if format == "html":
            return html
        elif format == "png":
            return Response(
                await screenshot(html, type="png"), mimetype="image/png")
        elif format in ["jpg", "jpeg"]:
            return Response(
                await screenshot(html, type="jpeg", quality=100),
                mimetype="image/jpeg")
        else:
            return abort(400)

    else:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://snowflake.breq.dev/") as response:
                card_id = str((await response.json())["snowflake"])

        os.mkdir(os.path.join(STORAGE_PATH, card_id))

        with open(os.path.join(STORAGE_PATH, card_id, "card.html"), "w") as f:
            f.write(html)

        async with open_html(html) as page:
            await page.screenshot(
                {
                    "type": "png",
                    "path": os.path.join(STORAGE_PATH, card_id, "card.png")
                }
            )
            await page.screenshot(
                {
                    "type": "jpeg",
                    "quality": 100,
                    "path": os.path.join(STORAGE_PATH, card_id, "card.jpeg")
                }
            )

        return jsonify({
            "card_id": card_id
        })


@app.route("/card/<string:card_id>.<string:format>")
async def card_by_id(card_id, format):
    if format == "jpg":
        format = "jpeg"
    if format not in ["html", "png", "jpeg"]:
        return abort(404)
    return await send_file(
        os.path.join(STORAGE_PATH, card_id, f"card.{format}"))


if __name__ == "__main__":
    app.run()
