import os
import re
import io
import asyncio
import contextlib
import aiohttp
import dotenv

from quart import (Quart, request, redirect, render_template, abort, Response, jsonify)
from markupsafe import Markup
from quart_cors import cors, route_cors

from minio import Minio

from pyppeteer import launch

dotenv.load_dotenv()

CHROME_PATH = os.environ.get('GOOGLE_CHROME_SHIM')
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")


app = Quart(__name__)
app = cors(app)


minio = Minio(
    MINIO_ENDPOINT,
    access_key=os.environ.get("MINIO_ACCESS_KEY"),
    secret_key=os.environ.get("MINIO_SECRET_KEY"),
)


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

    if request.method == "POST":
        async with aiohttp.ClientSession() as session:
            async with session.post("https://snowflake.breq.dev/") as response:
                card_id = str((await response.json())["snowflake"])

        minio.put_object(
            "cards",
            f"{card_id}.html",
            io.BytesIO(html.encode("utf-8")),
            len(html)
        )

        async with open_html(html) as page:
            png = await page.screenshot({"type": "png"})
            minio.put_object(
                "cards", f"{card_id}.png", io.BytesIO(png), len(png))

            jpeg = await page.screenshot({"type": "jpeg", "quality": 100})
            minio.put_object(
                "cards", f"{card_id}.jpeg", io.BytesIO(jpeg), len(jpeg))

        return jsonify({
            "card_id": card_id
        })
    else:
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


@app.route("/card/<string:card_id>.<string:format>")
async def card_by_id(card_id, format):
    if format == "jpg":
        format = "jpeg"
    if format not in ["html", "png", "jpeg"]:
        return abort(404)
    return Response(
        minio.get_object("cards", f"{card_id}.{format}").read(),
        mimetype=(
            "image/" + format if format in ["png", "jpeg"] else "text/html"
        )
    )


if __name__ == "__main__":
    app.run()
