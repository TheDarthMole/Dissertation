import "../vendor/codemirror-5.65.2/lib/codemirror.js";
import "../vendor/codemirror-5.65.2/mode/xml/xml.js"


var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    theme: "dracula",
    mode: "xml",
    lineNumbers: true
});

editor.setSize("500", "150");

//<textarea id="editor"></textarea>