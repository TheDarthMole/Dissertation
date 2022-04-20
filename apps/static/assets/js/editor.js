import {EditorState, EditorView, basicSetup} from "@codemirror/basic-setup"
import {java} from "@codemirror/lang-java"


    // <script src="webjars/codemirror/5.22.0/lib/codemirror.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/mode/clike/clike.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/mode/diff/diff.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/dialog/dialog.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/search/searchcursor.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/search/search.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/scroll/annotatescrollbar.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/search/matchesonscrollbar.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/search/jump-to-line.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/selection/active-line.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/edit/matchbrackets.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/edit/closebrackets.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/hint/show-hint.js" type="text/javascript" ></script>
    // <script src="webjars/codemirror/5.22.0/addon/hint/anyword-hint.js" type="text/javascript" ></script>


var editor_element = document.getElementById('editor');

// Convert from base64
var original_code = atob(editor_element.textContent);
editor_element.textContent='';


let editor = new EditorView({
  state: EditorState.create({
    extensions: [
        basicSetup,
        java(),

    ],
    doc: original_code
  }),
  parent: editor_element
})



document.getElementById('submit_code').addEventListener("click", ()=> {
    // submitting the code
    let code = editor.state.doc.toString();
    let b64code = btoa(code);

    // Add the encoded form text to be sent to the server
    // We do this hacky way of editing a form element instead of doing it all in JS
    // Because of Django's need for a CSRF token
    let form_code_input = document.getElementById('form_b64_code');

    console.log(form_code_input)
    form_code_input.value = b64code;

    console.log(form_code_input.value);

    // Submit the form
    document.code_submission_form.submit()

})
