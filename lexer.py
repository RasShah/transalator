import re

TOKEN_SPECIFICATION = [
    ("INT",       r'\bint\b'),
    ("BOOL",      r'\bbool\b'),
    ("TRUE",      r'\bTRUE\b'),
    ("FALSE",     r'\bFALSE\b'),
    ("ID",        r'[A-Za-z_]\w*'),
    ("NUMBER",    r'\d+'),
    ("PLUS",      r'\+'),
    ("MINUS",     r'-'),
    ("STAR",      r'\*'),
    ("SLASH",     r'/'),
    ("ASSIGN",    r'='),
    ("COMMA",     r','),
    ("SEMICOLON", r';'),
    ("LPAREN",    r'\('),
    ("RPAREN",    r'\)'),
    ("SKIP",      r'[ \t\n]+'),
    ("MISMATCH",  r'.'),
]


class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


def lexer(code):
    token_regex = '|'.join(
        f'(?P<{name}>{pattern})'
        for name, pattern in TOKEN_SPECIFICATION
    )

    get_token = re.compile(token_regex).match

    pos = 0
    line = 1
    col = 1

    mo = get_token(code, pos)

    while mo:
        typ = mo.lastgroup
        val = mo.group(typ)

        start_line = line
        start_col = col

        if typ == "SKIP":
            pass
        elif typ == "MISMATCH":
            raise RuntimeError(f'Unexpected character {val!r} at {line}:{col}')
        else:
            yield Token(typ, val, start_line, start_col)

        pos = mo.end()

        if '\n' in val:
            line += val.count('\n')
            col = len(val.rsplit('\n', 1)[-1]) + 1
        else:
            col += len(val)

        mo = get_token(code, pos)

    yield Token("EOF", "", line, col)