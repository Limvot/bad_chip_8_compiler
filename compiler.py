from enum import Enum
import re
import sys

if len(sys.argv) != 3:
    print("Need exactly one input file and one output file")
    sys.exit(1)

token_re = [
    ("whitespace", r'\s+'),
    ("(", r'\('),
    (",", r','),
    (")", r'\)'),
    ("{", r'\{'),
    ("}", r'\}'),
    ("=", r'='),
    ("==", r'=='),
    ("+=", r'\+='),
    ("-=", r'-='),
    ("void", r'void'),
    ("byte", r'byte'),
    ("inline_asm", r'inline_asm'),
    ("return", r'return'),
    ("if", r'if'),
    ("else", r'else'),
    ("while", r'while'),
    ("num", r'(0x[0-9A-F]+)|([0-9]+)'),
    ("reg", r'(v[0-9A-F])|I'),
    ("ident", r'\w+'),
    ("asm_body", r'#[^#]*#'),
]
token_re = list(map(lambda t: (t[0], re.compile(t[1], re.MULTILINE)), token_re))
def tokenize(input):
    i = 0
    tokens = []
    while i != len(input):
        longest_idx = -1
        longest_end = -1
        for (token_idx, (r_name, r)) in enumerate(token_re):
            maybe_match = r.match(input, i)
            if maybe_match:
                if maybe_match.end() > longest_end:
                    longest_end = maybe_match.end()
                    longest_idx = token_idx
        if longest_idx == -1:
            print("No token matched input starting with", input[i:])
            sys.exit(1)
        tokens.append((token_re[longest_idx][0], input[i:longest_end]))
        i = longest_end
    return tokens

with open(sys.argv[1], "rt") as f:
    tokens = tokenize(f.read())
tokens = list(filter(lambda x: x[0] != "whitespace", tokens))
print(tokens)

def assert_get(tokens, i, type):
    if isinstance(type, list):
        for t in type:
            if tokens[i][0] == t:
                return (i+1, tokens[i][1])
        print("got a " + tokens[i][0] + ", which was " + tokens[i][1] + " instead one of " + str(type))
        sys.exit(1)
    if tokens[i][0] != type:
        print("got a " + tokens[i][0] + ", which was " + tokens[i][1] + " instead of " + type)
        sys.exit(1)
    return (i+1, tokens[i][1])

def parse_file(tokens):
    i = 0
    to_ret = []
    while i < len(tokens):
        (i, f) = parse_function(tokens, i)
        to_ret.append(f)
    return to_ret
def parse_function(tokens, i):
    (i, type) = assert_get(tokens, i, ["void", "byte"])
    (i, name) = assert_get(tokens, i, "ident")
    (i, _) = assert_get(tokens, i, "(")
    params = []
    while tokens[i][0] != ")":
        (i, param) = assert_get(tokens, i, "ident")
        params.append(param)
        if tokens[i][0] != ")":
            (i, _) = assert_get(tokens, i, ",")
    (i, _) = assert_get(tokens, i, ")")
    (i, _) = assert_get(tokens, i, "{")
    body = []
    while tokens[i][0] != "}":
        (i, s) = parse_statement(tokens, i)
        body.append(s)
    (i, _) = assert_get(tokens, i, "}")
    return (i, {"name": name, "params": params, "body": body})
def parse_statement(tokens, i):
    print("Now parsing statement")
    if tokens[i][0] == "inline_asm":
        (i, _) = assert_get(tokens, i, "inline_asm")
        params = []
        (i, _) = assert_get(tokens, i, "(")
        while tokens[i][0] != ")":
            (i, reg) = assert_get(tokens, i, "reg")
            (i, _) = assert_get(tokens, i, "=")
            (i, value) = parse_value(tokens,i)
            params.append( (reg, value) )
            if tokens[i][0] != ")":
                (i, _) = assert_get(tokens, i, ",")
        (i, _) = assert_get(tokens, i, ")")
        (i, body) = assert_get(tokens, i, "asm_body")
        return (i, {"type": "inline_asm", "params": params, "body": body})
    elif tokens[i][0] == "byte":
        # this is a local variable declaration
        (i, _) = assert_get(tokens, i, "byte")
        (i, name) = assert_get(tokens, i, "ident")
        return (i, {"type": "declaration", "name": name})
    elif tokens[i][0] == "ident":
        # either a variable assignment, a function call
        if tokens[i+1][0] == "(":
            # function call
            (i, name) = assert_get(tokens, i, "ident")
            params = []
            (i, _) = assert_get(tokens, i, "(")
            while tokens[i][0] != ")":
                (i, value) = parse_value(tokens, i)
                params.append( value )
                if tokens[i][0] != ")":
                    (i, _) = assert_get(tokens, i, ",")
            (i, _) = assert_get(tokens, i, ")")
            return (i, {"type": "call", "name": name, "params": params})
        else:
            (i, name) = assert_get(tokens, i, "ident")
            (i, op) = assert_get(tokens, i, ["=", "+=", "-="])
            (i, value) = parse_value(tokens, i)
            return (i, {"type": "assign", "name": name, "op": op, "value": value})
    elif tokens[i][0] == "return":
        (i, _) = assert_get(tokens, i, "return")
        (i, _) = assert_get(tokens, i, "(")
        if tokens[i][0] != ")":
            (i, value) = parse_value(tokens,i)
        else:
            value = {"type":"num", "raw": "0"}
        (i, _) = assert_get(tokens, i, ")")
        return (i, {"type": "return", "value": value})
    elif tokens[i][0] == "if":
        (i, _) = assert_get(tokens, i, "if")
        (i, _) = assert_get(tokens, i, "(")
        (i, cond) = parse_value(tokens,i)
        (i, _) = assert_get(tokens, i, ")")
        (i, _) = assert_get(tokens, i, "{")
        than_body = []
        while tokens[i][0] != "}":
            (i, s) = parse_statement(tokens, i)
            than_body.append(s)
        (i, _) = assert_get(tokens, i, "}")
        else_body = []
        if tokens[i][0] == "else":
            (i, _) = assert_get(tokens, i, "else")
            (i, _) = assert_get(tokens, i, "{")
            while tokens[i][0] != "}":
                (i, s) = parse_statement(tokens, i)
                else_body.append(s)
            (i, _) = assert_get(tokens, i, "}")
        return (i, {"type": "if", "cond": cond, "than": than_body, "else": else_body})
    elif tokens[i][0] == "while":
        (i, _) = assert_get(tokens, i, "while")
        (i, _) = assert_get(tokens, i, "(")
        (i, cond) = parse_value(tokens,i)
        (i, _) = assert_get(tokens, i, ")")
        (i, _) = assert_get(tokens, i, "{")
        body = []
        while tokens[i][0] != "}":
            (i, s) = parse_statement(tokens, i)
            body.append(s)
        (i, _) = assert_get(tokens, i, "}")
        return (i, {"type": "while", "cond": cond, "body": body})
    else:
        print(tokens[i][1] + "(" + tokens[i][0] + ")" + " is not a statement")
        sys.exit(1)
def parse_value(tokens, i):
    to_ret = None
    if tokens[i][0] == "num":
        (i, num) = assert_get(tokens, i, "num")
        to_ret = {"type": "num", "raw": num}
    elif tokens[i][0] == "ident":
        (i, name) = assert_get(tokens, i, "ident")
        to_ret = {"type": "var", "name": name}
    else:
        print(tokens[i][1] + "(" + tokens[i][0] + ")" + " is not a value")
        sys.exit(1)
    if tokens[i][0] == "==":
        (i, op) = assert_get(tokens, i, "==")
        (i, other) = parse_value(tokens, i)
        return (i, {"type": "op", "op": op, "values": [to_ret, other]}) 
    else:
        return (i, to_ret)

my_special_id = 0
def get_id():
    global my_special_id
    my_special_id += 1
    return "id" + str(my_special_id)

def emit_save_regs():
    save = ""
    restore = ""
    save_label = "savelabel" + get_id()
    after_label = "afterlabel" + get_id()
    save += "imovi " + save_label + "\n"
    save += "store vF" + "\n"
    save += "jump " + after_label + "\n"
    save += save_label + ":\n"
    save += "movr v0 v0\n" * 16
    save += after_label + ":\n"
    restore += "imovi " + save_label + "\n"
    restore += "load vF\n"
    return (save, restore)

def emit(tree):
    to_ret = ""
    for t in tree:
        if t["name"] == "main":
            to_ret += emit_function(t, {}) + "\n"
    for t in tree:
        if t["name"] != "main":
            to_ret += emit_function(t, {}) + "\n"
    return to_ret

def emit_function(f, scope):
    new_scope = {}
    new_scope.update(scope)
    new_scope.update({ p: "v"+hex(i+3)[2:] for (i, p) in enumerate(f["params"])})
    to_ret = f["name"] + ":\n"
    for s in f["body"]:
        to_ret += emit_statement(s, new_scope)
    return to_ret

def emit_statement(s, scope):
    if s["type"] == "return":
        return emit_value(s["value"], scope) + "return\n"
    elif s["type"] == "declaration":
        for i in range(3, 16):
            name = "v"+hex(i)[2:]
            if name not in scope.values():
                scope[s["name"]] = name
                break
        else:
            print("couldn't find a free register for variable " + name + ", scope is " + str(scope))
            sys.exit(1)
        return ""
    elif s["type"] == "assign":
        to_ret = emit_value(s["value"], scope)
        if s["op"] == "=":
            to_ret += "movr " + scope[s["name"]] + " v0\n"
        elif s["op"] == "+=":
            to_ret += "addr " + scope[s["name"]] + " v0\n"
        elif s["op"] == "-=":
            to_ret += "subr " + scope[s["name"]] + " v0\n"
        else:
            print("assign does not support op " + s["op"])
            sys.exit(1)
        return to_ret
    elif s["type"] == "inline_asm":
        to_ret = ""
        (save, restore) = emit_save_regs()
        to_ret += save
        for (reg, value) in s["params"]:
            to_ret += emit_value(value, scope)
            to_ret += "movr " + reg + " v0\n"
        to_ret += s["body"][1:-1]
        to_ret += restore
        return to_ret
    elif s["type"] == "call":
        to_ret = ""
        (save, restore) = emit_save_regs()
        to_ret += save
        for (i, v) in enumerate(s["params"]):
            to_ret += emit_value(v, scope)
            to_ret += "movr v" + str(i+1) + " v0\n"
        return to_ret + "call " + s["name"] + "\n" + restore
    elif s["type"] == "if":
        afterthan = "afterthan" + get_id()
        afterelse = "afterelse" + get_id()
        to_ret = emit_value(s["cond"],scope)
        to_ret += "snei v0 0\n"
        to_ret += "jump " + afterthan + "\n"

        new_scope = {}
        new_scope.update(scope)
        for si in s["than"]:
            to_ret += emit_statement(si, new_scope)
        to_ret += "jump " + afterelse + "\n"
        to_ret += afterthan + ":\n"
        new_scope = {}
        new_scope.update(scope)
        for si in s["else"]:
            to_ret += emit_statement(si, new_scope)
        to_ret += afterelse + ":\n"
        return to_ret
    elif s["type"] == "while":
        whiletop = "whiletop" + get_id()
        whileend = "whileend" + get_id()
        to_ret = whiletop + ":\n"
        to_ret += emit_value(s["cond"], scope)
        to_ret += "snei v0 0\n"
        to_ret += "jump " + whileend + "\n"
        new_scope = {}
        new_scope.update(scope)
        for si in s["body"]:
            to_ret += emit_statement(si, new_scope)
        to_ret += "jump " + whiletop + "\n"
        to_ret += whileend + ":\n"
        return to_ret
    else:
        print("what sort of statement is " + str(s))
        sys.exit(1)

def emit_value(v, scope):
    if v["type"] == "num":
        return "movi v0 " + v["raw"] + "\n"
    elif v["type"] == "var":
        return "movr v0 " + scope[v["name"]] + "\n"
    elif v["type"] == "op":
        to_ret = emit_value(v["values"][0], scope)
        to_ret += "movr v1 v0\n"
        to_ret += emit_value(v["values"][1], scope)
        to_ret += "movr v2 v0\n"
        if v["op"] == "==":
            to_ret += "movi v0 0\n"
            to_ret += "sner v1 v2\n"
            to_ret += "movi v0 1\n"
        else:
            print("cannot emit op " + v["op"])
            sys.exit(1)
        return to_ret
    else:
        print("what sort of value is " + str(v))
        sys.exit(1)

tree = parse_file(tokens)
asm = emit(tree)
asm = " \n".join(asm.splitlines())
print("; calling convention")
print("; v0 is scratch, unsaved, and used for return")
print("; v1-vF is for parameters, and are unsaved")
print(asm)
with open(sys.argv[2], "wt") as f:
    f.write(asm)
