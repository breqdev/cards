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

import boto3

from pyppeteer import launch

dotenv.load_dotenv()

CHROME_PATH = os.environ.get('GOOGLE_CHROME_SHIM')

S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_BUCKET = os.environ.get("S3_BUCKET", "cards")
S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")



app = Quart(__name__)
app = cors(app)


s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
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
    return redirect("https://cards.breq.dev")


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

        s3.put_object(
            Bucket=S3_BUCKET,
            Key=f"{card_id}.html",
            Body=io.BytesIO(html.encode("utf-8"))
        )

        async with open_html(html) as page:
            png = await page.screenshot({"type": "png"})
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=f"{card_id}.png",
                Body=io.BytesIO(png)
            )

            jpeg = await page.screenshot({"type": "jpeg", "quality": 100})
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=f"{card_id}.jpeg",
                Body=io.BytesIO(jpeg)
            )

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
        s3.get_object(
            Bucket=S3_BUCKET,
            Key=f"{card_id}.{format}"
        )["Body"].read(),

        mimetype=(
            "image/" + format if format in ["png", "jpeg"] else "text/html"
        )
    )


if __name__ == "__main__":
    app.run()
