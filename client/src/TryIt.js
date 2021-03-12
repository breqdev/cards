import React from "react"

import Configurator from "./Configurator"
import CardOutput from "./CardOutput"

export default function TryIt(props) {
    const [cardURL, setCardURL] = React.useState(
        "https://cards.api.breq.dev/card/130828557977848352.html")

    function makeCardURL({name, bio, image, format}) {
        let url = "https://cards.api.breq.dev/card?"
        let params = new URLSearchParams({
            name,
            bio,
            background_image: image,
            template: "background-image",
            format
        })

        url += params.toString()
        return url
    }

    const onUpdate = (params) => {
        let newURL = makeCardURL(params)
        setCardURL(newURL)
    }

    const onFreeze = (params) => {
        let newURL = makeCardURL(params)

        fetch(newURL, {method: "POST"})
            .then(response => response.json())
            .then(response => setCardURL(
                `https://cards.api.breq.dev/card/${response.card_id}.html`
            ))
    }

    return (
        <div style={{display: "flex", flexWrap: "wrap"}}>
            <Configurator onUpdate={onUpdate} onFreeze={onFreeze} />
            <div className="separator"> </div>
            <CardOutput cardURL={cardURL} />
        </div>
    )
}
