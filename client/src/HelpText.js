import React from "react"

export default function HelpText(props) {
    return (
        <div>
            <h1>Getting a card</h1>

            <p>Send a GET request to <code>https://cards.api.breq.dev/card</code> with some of the following parameters:</p>

            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>format</td>
                    <td>Format of the returned card (html, png, jpeg)</td>
                </tr>
                <tr>
                    <td>template</td>
                    <td>Template used to generate the card (background-image, basic)</td>
                </tr>
            </table>

            <p>In addition, each template has some of its own parameters. For instance, the background-image template takes:</p>

            <table>
                <tr>
                    <td>name</td>
                    <td>Name printed in large text on the card</td>
                </tr>
                <tr>
                    <td>bio</td>
                    <td>Description printed in smaller text</td>
                </tr>
                <tr>
                    <td>background_image</td>
                    <td>Image in the top half of the card</td>
                </tr>
            </table>

            <h1>Freezing a card</h1>

            <p>If you send a POST to that URL instead, your card will be "frozen": rendered on the server and stored there. The server will send back a JSON response with <code>{'{"card_id": 130810678565865982}'}</code> (or whatever your ID is). Then, send a GET to <code>https://cards.api.breq.dev/card/[id].html</code> or <code>.png</code> or <code>.jpg</code> to get the card.</p>

            <p><strong>Freezing cards is a good idea.</strong> It will reduce the server load, since the server won't have to re-render the card every time it gets served. It will also speed up your app, since it won't have to wait for the server to render the card before displaying it to the user.</p>

            <h1>Embedding a card</h1>

            <p><strong>Can you use HTML?</strong> - Include an IFrame linking to the card.</p>

            <code>{'<iframe height="300" width="500" src="https://cards.api.breq.dev/card?format=html&template=background-image&name=IFrame Card&bio=Card embedded in a webpage using an iframe.&background_image=https://breq.dev/opengraph/pansexual.jpg"></iframe>'}</code>

            <br />

            <iframe title="HTML card" style={{border: "none"}} height="300" width="500" src="https://cards.api.breq.dev/card/219156081436576520.html" />

            <p><strong>Otherwise, use images</strong> - Use a basic <code>{'<img>'}</code> tag, or markdown.</p>

            <code>{'![](https://cards.api.breq.dev/card?format=png&template=background-image&name=Rendered Card&bio=Card rendered on the server and included as a PNG.&background_image=https://breq.dev/opengraph/pansexual.jpg)`'}</code>

            <br />

            <img src="https://cards.api.breq.dev/card/130828557977848352.png" alt="PNG card" />

            <p>If you can, use IFrames. This reduces server-side load, speeding up your app.</p>

            <h1>Styling Tips</h1>

            <p>Add a `border-radius: 15px` to the IFrame for some nice, rounded corners:</p>

            <iframe title="Rounded edges card" style={{border: "none", borderRadius: "15px"}} height="300" width="500" src="https://cards.api.breq.dev/card/219156300446354185.html" />

            <br />

        </div>
    )
}