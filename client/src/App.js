import React from "react"
import { Page, Heading } from "@breq/react-theme"
import { faGithub, faKeybase } from "@fortawesome/free-brands-svg-icons"

import TryIt from "./TryIt"
import HelpText from "./HelpText"

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
            <Heading title="Cards" subtitle="Generate and embed digital cards featuring custom images and text." />
            <TryIt />
            <hr />
            <HelpText />
        </Page>
    )
}
