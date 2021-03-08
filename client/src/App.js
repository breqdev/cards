import React from "react"
import { Page } from "@breq/react-theme"
import { faKeybase } from "@fortawesome/free-brands-svg-icons"

const links = {
    github: "https://github.com/breq16"
}

const contact = [
    {
        text: "breq",
        icon: faKeybase,
        link: "https://keybase.io/breq"
    }
]

export default function App(props) {
    return (
        <Page brand="cards by breq" links={links} contact={contact} author="breq" copyright="2021" repo="Breq16/cards">
            <h1>Hello World!</h1>
            <p><i>Live demo coming soon...</i></p>
            <br />
            <p>In the meantime, check out the demo on <a href="https://breq.dev/apps/cards/">breq.dev</a>.</p>
        </Page>
    )
}
