import React from "react"

import styles from "./CardOutput.module.scss"

function URLOutput(props) {
    const inputStyle = {
        boxSizing: "border-box",
        width: "100%",
        color: "black",
        textAlign: "center",
        marginRight: "10px"
    }

    const handleClick = (e) => navigator.clipboard.writeText(props.url)

    return (
        <div className={styles.urlOutput}>
            <input
                type="text"
                value={props.url}
                className={styles.urlOutputInput}
                disabled
            />
            <button
                className={styles.button}
                type="button"
                onClick={handleClick}
            >Copy</button>
        </div>
    )
}

export default function CardOutput(props) {
    const style = {
        textAlign: "center",
        width: "500px",
        padding: "20px",
        margin: "auto",
        border: "2px solid black"
    }

    return (
        <div style={style}>
            <h1>Rendered Card</h1>
            <iframe height="300" width="500" title="card" src={props.cardURL} />
            <br />
            <URLOutput url={props.cardURL} />
        </div>
    )
}
