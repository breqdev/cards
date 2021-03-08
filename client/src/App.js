import React from "react"
import { Page } from "@breq/react-theme"
import { faGithub, faKeybase } from "@fortawesome/free-brands-svg-icons"

import TryIt from "./TryIt"

const links = {
    github: "https://github.com/breq16/cards"
}

const contact = [
    {
        text: "breq",
        icon: faKeybase,
        link: "https://keybase.io/breq"
    },
    {
        text: "breq16",
        icon: faGithub,
        link: "https://github.com/breq16"
    }
]

export default function App(props) {
    return (
        <Page
            brand="cards by breq"
            links={links}
            contact={contact}
            author="breq"
            copyright="2021"
            repo="Breq16/cards"
        >
            <div style={{textAlign: "center", marginTop: "15px"}}>
                <h1 style={{fontSize: "72px", marginBottom: "10px"}}>Cards</h1>
                <p>Generate and embed digital cards featuring custom images and text.</p>
            </div>
            <br />
            <TryIt />
        </Page>
    )
}
