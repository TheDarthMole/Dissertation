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

