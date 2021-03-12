import React from "react"

import { Input, Button } from "@breq/react-theme"

function URLOutput(props) {
    const handleClick = (e) => navigator.clipboard.writeText(props.url)

    return (
        <div style={{display: "flex", width: "100%"}}>
            <Input style={{flexGrow: 1}} value={props.url} disabled />
            <Button style={{width: "max-content"}} onClick={handleClick}>Copy</Button>
        </div>
    )
}

export default function CardOutput(props) {
    return (
        <div style={{maxWidth: "100%"}}>
            <h1>Rendered Card</h1>
            <div style={{display: "block", overflow: "auto"}}>
                <iframe height="300" width="500" frameBorder="0" title="card" src={props.cardURL} />
            </div>
            <URLOutput url={props.cardURL} />
        </div>
    )
}
