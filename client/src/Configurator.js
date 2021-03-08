import React from "react"

import styles from "./Configurator.module.scss"

function InputGroup(props) {
    const handleChange = (e) => props.onChange(e.target.value)

    return (
        <div className={styles.inputGroup}>
            <label className={styles.label}>{props.label}</label>
            <input
                className={styles.input}
                type="text"
                value={props.value}
                onChange={handleChange}
            />
        </div>
    )
}

export default function Configurator(props) {
    const [name, setName] = React.useState("My Awesome Card")
    const [bio, setBio] = React.useState(
        "This is the description that will go on my card")
    const [image, setImage] = React.useState(
        "https://breq.dev/assets/images/pansexual.png")

    const state = {
        name,
        bio,
        image,
        format: "html"
    }

    return (
        <div>
            <form onSubmit={(e) => {e.preventDefault()}}>
                <InputGroup
                    key="Name"
                    label="Name"
                    value={name}
                    onChange={setName}
                />
                <InputGroup
                    key="Bio"
                    label="Bio"
                    value={bio}
                    onChange={setBio}
                />
                <InputGroup
                    key="Image URL"
                    label="Image URL"
                    value={image}
                    onChange={setImage}
                />
                <div className={styles.buttonGroup}>
                    <button
                        className={styles.button}
                        onClick={() => props.onUpdate(state)}
                    >
                        Update
                    </button>
                    <button
                        className={styles.button}
                        onClick={() => props.onFreeze(state)}
                    >
                        Freeze
                    </button>
                </div>
            </form>
        </div>
    )
}
