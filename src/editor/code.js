var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    autocorrect: true,
    dragDrop: true,
    mode: "python",
    theme: "default",
    extraKeys: {
        "Ctrl-Space": "autocomplete"
    }
});

editor.setSize("100%", "100%");