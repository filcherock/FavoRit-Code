from pickledb import PickleDB

config = PickleDB('config.json')
keywords = config.get('syntax_keyword')
funcs = config.get('syntax_func')
string = config.get('syntax_str')
comments = config.get('syntax_comment')

repl = [
    [r'\b(True|False|None|and|as|assert|async|await|break|class|continue|def|del|elif|else|expect|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b', keywords],
    [r'\b(print|input|len|abs|sum|min|max|str|int|float|list|tuple|dict|range|enumerate|map|filter|zip|sorted|type|bool|chr)\b', funcs],
    [r'"[^"\\]*(?:\\.[^"\\]*)*"', string], 
    [r"'[^'\\]*(?:\\.[^'\\]*)*'", string], 
    ['#.*', comments],
]

ptext = ''