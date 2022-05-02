import {EditorState, EditorView, basicSetup} from "@codemirror/basic-setup"
import {java} from "@codemirror/lang-java"
import {Compartment} from "@codemirror/state"
import {keymap} from "@codemirror/view"
import {indentWithTab} from "@codemirror/commands"
import {CompletionContext, autocompletion} from "@codemirror/autocomplete"


const editor_element = document.getElementById('editor');
// Convert from base64
const original_code = atob(editor_element.textContent);
editor_element.textContent = '';
let tabSize = new Compartment


let state = EditorState.create({
    extensions: [
        basicSetup,
        java(),
        keymap.of([indentWithTab]),
        autocompletion(), // This doesn't work?
        // tabSize.of(EditorState.tabSize.of(4))
    ],
    tabSize: 8,
    doc: original_code
})

let editor = new EditorView({
    state: state,
    parent: editor_element
})


editor_element.removeAttribute("hidden");

document.getElementById('submit_code').addEventListener("click", () => {
    // submitting the code
    let code = editor.state.doc.toString();
    let b64code = btoa(code);

    // Add the encoded form text to be sent to the server
    // We do this hacky way of editing a form element instead of doing it all in JS
    // Because of Django's need for a CSRF token
    let form_code_input = document.getElementById('form_b64_code');

    form_code_input.value = b64code;

    // Submit the form
    document.code_submission_form.submit()

})
