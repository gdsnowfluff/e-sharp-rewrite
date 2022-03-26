import argparse,random

parser = argparse.ArgumentParser()
parser.add_argument("-d",type=bool,help="Debug mode. (Prints variables and tokens.)")
args = parser.parse_args()

variables = {'pi':"3.14159",'key':str(random.randint(0,9999999999))}

DIGITS = "0123456789"
OPERATORS = "+-*/"
STATES = ("true","false")

def lexer(text):
    tok = ""
    tmp = ""
    num = ""
    iS = False
    string = ""
    tokens = []
    tokens.append("SOF")
    for char in text:
        tok += char
        tmp += char
        if tok == " ":
            if iS:
                string+=tok
            tok = ""
        elif tok == "log(":
            tokens.append("print")
            tok = ""
        elif tok == "fart(":
            tokens.append("fart")
            tok = ""
        elif tok == ")":
            tokens.append("close")
            tok = ""
        elif tok == '"' or tok == "'":
            if iS == False:
                iS = True
                tok = ""
            else:
                iS = False
                tokens.append(f"string: {string}")
                string = ""
                tok = ""
        elif tok == "=" or tok[-1:] == "=":
            tokens.append(f"var {tmp[:-2]}")
            tokens.append("equals")
            tmp = ""
            tok = ""
        elif tok in DIGITS:
            num += tok
            tok = ""
        elif tok == "$":
            tokens.append(f"number: {int(num)}")
            num = ""
            tok = ""
        elif tok[-1:] == "#":
            tokens.append(f"ref: {tok[:-1]}")
            tok = ""
        elif tok in OPERATORS:
            tokens.append(tok)
            tok = ""
        elif tok in STATES:
            tokens.append("bool: "+tok)
            tok = ""
        elif tok == "if":
            tokens.append('if')
            tok = ""
        elif tok == "is":
            tokens.append("is")
            tok = ""
        elif tok == "do":
            tokens.append("do")
            tok = ""
        elif tok == "endif":
            tokens.append("close")
            tok = ""
        else:
            if iS:
                string+=tok
                tok=""
    tokens.append("EOF")
    return tokens

def parser(toks):
    i = 0
    try:
        while i < len(toks):
            if toks[i] != "EOF":
                if toks[i] == "print":
                    if toks[i+1][0:6] == "string":
                        if toks[i+2] == "close":
                            print(toks[i+1][8:])
                        else:
                            raise SyntaxError("Didn't close log statement.")
                    elif toks[i+1][:3] == "ref":
                        if toks[i+2] == "close":
                            if variables[toks[i+1][5:]] != "":
                                print(variables[toks[i+1][5:]])
                            else:
                                raise ValueError("No variable named",toks[i+1][5:])
                        else:
                            raise SyntaxError("Didn't close log statement.")
                    else:
                        raise ValueError("Missing string argument.")
                elif f"{toks[i][:3]} {toks[i+1]}" == "var equals":
                    if toks[i+2][:6] == "string" or toks[i+2][:6] == "number":
                        value = toks[i+2][8:]
                        name = toks[i][4:]
                        variables[name] = value
                    elif toks[i+2][:4] == 'bool':
                        value = toks[i+2][6:]
                        name = toks[i][4:]
                        variables[name] = value
                    else:
                        raise ValueError("Never assigned value, or used inappropriate keyword.")
                elif toks[i+1] in OPERATORS:
                    if toks[i][:3] == "ref":
                        a = variables[toks[i][5:]]
                    else:
                        a = toks[i][8:]
                    if toks[i+2][:3] == "ref":
                        c = variables[toks[i+2][5:]]
                    else:
                        c = toks[i+2][8:]
                    b = toks[i+1]
                    print(eval(f"{a}{b}{c}"))
                elif toks[i] == "fart":
                    if toks[i+1][:6] == "string" and toks[i+2] == "close":
                        print(f"{toks[i+1][8:]} farted")
            i+=1
    except Exception as e:
        print(e)

def run():
    while True:
        b = input("E SHARP ~ ")
        b = str(b)
        c = lexer(b)
        parser(c)
        if args.d == True:
            print(c,variables)

run()