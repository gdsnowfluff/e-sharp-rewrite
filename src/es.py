variables = {'pi':'fart','why':'yes'}
keywords = ['print','exit','var','atom','help','all','import']
imports = []

def lexer(text):
    tokens = ['SOF']
    tok = ""
    string = ""
    name = ''
    iS = False
    digits = '0123456789'
    literals = "= '#()"
    operands = '+-*/'
    jENM = False
    iN = False
    nmin = False
    tmp = ""
    for char in text:
        tok += char
        tmp += char
        if tok in literals or tok[-1:] in literals:
            if tok == " " or tok[-1:] == ' ':
                if iS:
                    string+=tok
                elif iN:
                    iN = False
                    tokens.append("num:"+str(int(tmp[:-1])))
                    tmp = ""
                elif nmin:
                    if jENM:
                        tok = ""
                        jENM = False
                    else:
                        tokens.append('tin:'+name)
                        nmin = False
                        name = ''
                        tok = ""
                tok = ""
            elif tok == "'":
                if iS:
                    tokens.append('str:'+string)
                    iS = False
                    string = ""
                    tok = ""
                else:
                    iS = True
                    tok = ""
            elif tok == '=':
                tokens.append('as')
                tok = ''
            elif tok[-1:] == "#":
                tokens.append('ref:'+tok[:-1])
                tok = ""
            elif tok == '(':
                tokens.append("ver:0")
                tok = ""
            elif tok[-1:] == ")":
                if iN:
                    iN = False
                    tokens.append("num:"+str(int(tmp[:-1])))
                    tmp = ""
                tokens.append('clv')
                tok = ""
        elif str(tok) in digits:
            if iN:
                tok = ""
            elif iN == False:
                if nmin == False:
                    tmp = ""
                    tmp+=tok
                    tok = ""
                    iN = True
                else:
                    tmp += tok
        elif tok == '\n':
            if iN:
                iN = False
                tokens.append("num:"+str(int(tmp)))
                tmp = ""
            tokens.append("n")
            tok = ""
        elif tok == "\t":
            tokens.append('t')
            tok = ""
        elif tok in operands:
            if iN:
                iN = False
                tokens.append("num:"+str(int(tmp[:-1])))
                tmp = ""
            tokens.append(tok)
            tok = ""
        elif tok in keywords:
            tokens.append(tok)
            if tok == 'var':
                nmin = True
                jENM = True
            tok = ""
        else:
            if iS:
                string+=tok
                tok = ""
            elif nmin:
                name += tok
                tok = ""
    if iN:
        iN = False
        tokens.append("num:"+str(int(tmp)))
        tok = ""
        tmp = ""
    tokens.append('EOF')
    #print(tokens)
    return tokens

def parser(toks):
    def __ver__(a,b,c,e):
        a = str(a[4:])
        b = str(b)
        c = str(c[4:])
        d = eval(a+b+c)
        toks[e+1] = 'num:'+str(d)
        toks[e+2] = None
        toks[e+3] = None
        toks[e+4] = None
        toks[e+5] = None
    operands = "+-*/"
    i = 0
    while i < len(toks):
        if toks[i] != "EOF":
            if toks[i] == "print":
                if toks[i+1][:3] == 'str' or toks[i+1][:3] == 'num':
                    print(toks[i+1][4:])
                elif toks[i+1][:3] == 'ref':
                    print(variables[toks[i+1][4:]])
                elif toks[i+1][:3] == 'ver':
                    __ver__(toks[i+2],toks[i+3],toks[i+4],i)
                    print(toks[i+1][4:])
                elif toks[i+1] == 'atom':
                    b = input('What is your compiler?\n')
                    if b == 'ei':
                        print("EI - E Interperator\n\nThe official E compiler.")
                    elif b == 'gcc':
                        print('GCC - C Compiler\n\nHow are you using this for E?')
                    else:
                        print('Couldn\'t find any information on ',b.upper(),".", sep = "")
                elif toks[i+1] == 'help':
                    a = open('grammar.txt','r').read()
                    print(a)
                elif toks[i+1] == 'all':
                    print(keywords)
            elif toks[i] == 'exit':
                mes = 'Thank you. Goodbye!'
                if toks[i+1][:3] == 'str':
                    mes = toks[i+1][4:]
                exit(mes)
            elif toks[i] == 'var':
                if toks[i+1][:3] == 'tin':
                    if toks[i+2] == 'as':
                        name = toks[i+1][4:]
                        if toks[i+3][:3] == 'ver':
                            __ver__(toks[i+4],toks[i+5],toks[i+6],i+2)
                        value = toks[i+3][4:]
                        variables[name] = value
            elif toks[i+1] == 'ver:0':
                a = toks[i+2][4:]
                b = toks[i+3]
                c = toks[i+4][4:]
                d = eval(a+b+c)
                toks[i+1] = 'num:'+str(d)
                toks[i+2] = None
                toks[i+3] = None
                toks[i+4] = None
                toks[i+5] = None
            elif toks[i+1] in operands:
                a = toks[i][4:]
                b = toks[i+2][4:]
                if toks[i][:3] == 'ref':
                    a = variables[toks[i][4:]]
                if toks[i+2][:3] == 'ref':
                    a = variables[toks[i+2][4:]]
                c = toks[i+1]
                print(eval(a+c+b))
            elif toks[i] == 'import':
                imports.append(toks[i+1][4:])
                    
        i+=1
    return toks

def run(text):
    a = lexer(text)
    b = parser(a)
    #print(variables,b)