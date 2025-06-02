// All globally accessible global variables and functions
let editor_content = {};
let monacoEditor;
let ex_lang_id = 0;

function set_default_code() {
    if (!confirm("Are you sure you want to reset the code?")) return;
    const lang_id = document.getElementById("lang_id").value;
    editor_content[lang_id].last_code = "";
    monacoEditor.setValue(editor_content[lang_id].default_code);
}

function set_solve_code(solve_code) {
    if (!confirm("Are you sure you want to load the solution?")) return;
    const lang_id = document.getElementById("lang_id").value;
    editor_content[lang_id].last_code = solve_code;
    monacoEditor.setValue(solve_code);
}

function save_current_code() {
    const lang_id = document.getElementById("lang_id").value;
    const currentCode = monacoEditor.getValue();
    editor_content[lang_id].last_code = currentCode;
    document.getElementById("raw_code").value = currentCode;
}

function check_test_result() {
    const formElement = document.getElementById("user_form");
    const data = new URLSearchParams(new FormData(formElement));

    disable_form(true);

    fetch('/exercise/stats_create/', {
        method: 'POST',
        body: data,
    })
    .then(response => response.json())
    .then(() => {
        disable_form(false);
    });
}

function disable_form(is_disable) {
    const fs = document.getElementById("field_set_form");
    if (is_disable) fs.setAttribute("disabled", "disabled");
    else fs.removeAttribute("disabled");
}

function switch_language() {
    display_result_stat();
    check_test_result();

    const lang_id = document.getElementById("lang_id").value;

    if (ex_lang_id !== 0) {
        editor_content[ex_lang_id].last_code = monacoEditor.getValue();
    }
    ex_lang_id = lang_id;

    const new_code = editor_content[lang_id].last_code || editor_content[lang_id].default_code;
    monacoEditor.setValue(new_code);

    const def_code = JSON.parse(document.getElementById("languages").textContent);
    const languageName = def_code[lang_id].monaco_name || def_code[lang_id].name.toLowerCase();
    monaco.editor.setModelLanguage(monacoEditor.getModel(), languageName);
}

// now, DOMContentLoaded for init
document.addEventListener("DOMContentLoaded", () => {
    const def_code = JSON.parse(document.getElementById("languages").textContent);

    for (const [key, value] of Object.entries(def_code)) {
        editor_content[key] = { default_code: value.default_code, last_code: "" };
    }

    // Init liste de langues
    const ulLangs = document.getElementById("languages_stats");
    for (const key in def_code) {
        if (def_code.hasOwnProperty(key)) {
            const li = document.createElement("li");
            li.textContent = def_code[key].name;
            ulLangs.appendChild(li);
        }
    }

    // Init éditeur
    const lang_id = document.getElementById("lang_id").value;
    editor_content[lang_id].last_code = editor_content[lang_id].default_code;
    document.getElementById("raw_code").value = editor_content[lang_id].default_code;

    require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.33.0/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        monacoEditor = monaco.editor.create(document.getElementById('monaco_container'), {
            value: '',
            language: 'javascript',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            wordWrap: 'on'
        });

        monacoEditor.setValue(editor_content[lang_id].default_code);
        switch_language();
    });

    // Submit = save
    document.getElementById("user_form").addEventListener("submit", function () {
        save_current_code();
    });

    display_result_stat();
    check_test_result();
});
