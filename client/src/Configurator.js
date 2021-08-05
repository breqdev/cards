import React from "react"

import { Form, FormGrid, LabelInput, LabelTextArea, LabelDropdown, Button, ButtonGroup } from "@breq/react-theme"

export default function Configurator(props) {
    const [name, setName] = React.useState("My Awesome Card")
    const [bio, setBio] = React.useState(
        "This is the description that will go on my card")
    const [image, setImage] = React.useState(
        "https://breq.dev/assets/images/pansexual.png")
    const [format, setFormat] = React.useState("html")

    const formats = {html: ".html", png: ".png", jpg: ".jpg"}

    const state = {
        name,
        bio,
        image,
        format
    }

    return (
        <div style={{flexGrow: 1}}>
            <Form style={{boxSizing: "border-box", width: "100%", border: "none"}}>
                <FormGrid>
                    <LabelInput
                        key="Name"
                        label="Name"
                        value={name}
                        onChange={setName}
                    />
                    <LabelTextArea
                        key="Bio"
                        label="Bio"
                        value={bio}
                        onChange={setBio}
                    />
                    <LabelInput
                        key="Image URL"
                        label="Image URL"
                        value={image}
                        onChange={setImage}
                    />
                    <LabelDropdown
                        key="Format"
                        label="Format"
                        options={formats}
                        value={format}
                        onChange={setFormat}
                    />
                </FormGrid>
                <ButtonGroup style={{display: "flex"}}>
                    <Button onClick={() => props.onUpdate(state)}>Update</Button>
                    <Button onClick={() => props.onFreeze(state)}>Freeze</Button>
                </ButtonGroup>
            </Form>
        </div>
    )
}
