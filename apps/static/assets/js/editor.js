import {EditorState, EditorView, basicSetup} from "@codemirror/basic-setup"
import {java} from "@codemirror/lang-java"

var editor_element = document.getElementById('editor');
// Convert from base64
var original_code = atob(editor_element.textContent);
editor_element.textContent='';


let editor1 = new EditorView({
  state: EditorState.create({
    extensions: [basicSetup, java()],
    doc: original_code
  }),
  parent: document.getElementById('editor')
})

console.log("heeyy")