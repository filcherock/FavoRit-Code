var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    lineNumbers: true,
    mode: "text/x-python",
    theme: "default",
    extraKeys: {
        "Ctrl-Space": "autocomplete"
    }
});

editor.setSize("100%", "100%");

// Список слов для автодополнения — можно дополнять
var pythonKeywords = [
    "import", "from", "class", "def", "if", "else", "elif",
    "while", "for", "in", "return", "try", "except", "finally",
    "with", "as", "lambda", "and", "or", "not", "is", "None",
    "True", "False", "print", "len", "range", "list", "dict",
    "set", "str", "int", "float", "open", "enumerate", "zip",
    "map", "filter", "sum", "min", "max", "math", "os", "sys"
];
var userFunctions = [];
var userVariables = [];

function addUserSymbol(name) {
    if (userFunctions.indexOf(name) === -1) {
        userFunctions.push(name);
    }
}

// Хелпер подсказок: возвращает список совпадений по текущему токену
function pythonHint(cm) {
    var cursor = cm.getCursor();
    var token = cm.getTokenAt(cursor);
    var start = token.start;
    var end = cursor.ch;
    // Получаем часть токена до курсора
    var cur = token.string.slice(0, end - start);

    // Если текущий токен не содержит букв/цифр/_ или точки — не показываем подсказки
    if (!/^[\w.]+$/.test(cur)) {


return { list, from: CodeMirror.Pos(cursor.line, end), to: CodeMirror.Pos(cursor.line, end) };
    }

    var lower = cur.toLowerCase();
    var list = pythonKeywords.filter(function(keyword) {
        return keyword.toLowerCase().startsWith(lower);
    });
    list = list.concat(userFunctions.filter(function(func) {
        return func.toLowerCase().startsWith(lower);
    }));

    list = list.concat(userVariables.filter(function(variable) {
        return variable.toLowerCase().startsWith(lower);
    }));

    // возвращаем диапазон, который будет заменён при выборе подсказки
    return {
        list: list,
        from: CodeMirror.Pos(cursor.line, start),
        to: CodeMirror.Pos(cursor.line, end)
    };
}

// Регистрируем helper для режима "python"
CodeMirror.registerHelper("hint", "python", pythonHint);

// Команда autocomplete, привязанная к Ctrl-Space через extraKeys
CodeMirror.commands.autocomplete = function(cm) {
    cm.showHint({ hint: CodeMirror.hint.python, completeSingle: false });
};

// Автопоказ подсказок при вводе букв/точек/подчёркиваний
// debounce, чтобы не дергать подсказки слишком часто
var acTimer = null;

editor.on("inputRead", function(cm, change) {
    if (change.origin === "setValue") return; // игнор программного вставления

    var text = change.text.join(""); // что фактически вставлено/введено
    // Если нет текста — ничего не делаем
    if (!text) return;

    // Триггерим автодополнение при вводе одного символа: буквы/цифры/подчёркивания/точки
    // или при удалении (backspace/delete) — чтобы подсказки обновлялись
    var isTypingTrigger = (text.length === 1 && /[\w.]/.test(text));
    var isDeletion = change.origin === "delete" || change.origin === "+delete" || change.origin === "cut";

    if (!isTypingTrigger && !isDeletion) return;

    clearTimeout(acTimer);
    acTimer = setTimeout(function() {
        // Показываем подсказки; completeSingle: false — не автозаменять при единственном варианте
        cm.showHint({ hint: CodeMirror.hint.python, completeSingle: false });
    }, 100); // задержку можно уменьшить (например до 50) для более быстрого отклика
});