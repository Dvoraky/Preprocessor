path = input("Digite o caminho do arquivo: ")
texto = []
index = []

with open(path, "r") as arquivo:
    texto = arquivo.readlines()

def imprimir(text):
    for linha in text:
        print(linha, end = "")

def RemoverEspaços(string):
    string_processada = ""
    palavras = string.replace(';','; ').replace('(', '( ').replace("{", "{ ").split()
    aspas = False

    for i, palavra in enumerate(palavras):
        if palavra.startswith('"') and len(palavra) > 1:
            aspas = True

        if aspas:
            string_processada += palavra + " "
        else:
            if i > 0 and palavras[i-1] in ["int", "float", "char", "return", "void", "unsigned", "double", "long", "short", "void"]:
                string_processada += " "
            string_processada += palavra

        if palavra.endswith('"'):
            aspas = False

    return string_processada.strip()

def ExpandirDefine(linha):
    aux = []
  
    aux = linha.split()
    variavel = "".join(aux[1])
    valor2 = "".join(aux[2])
    
    return variavel, valor2

def removerComentarios(texto):
    codigo_sem_comentarios = []
    comentario_aberto = False

    for linha in texto:
        linha_sem_comentarios = ""

        i = 0
        while i < len(linha):
            if not comentario_aberto and linha[i:i+2] == "//":
                break
            elif not comentario_aberto and linha[i:i+2] == "/*":
                comentario_aberto = True
                i += 2
                continue
            elif comentario_aberto and linha[i:i+2] == "*/":
                comentario_aberto = False
                i += 2
                continue
            elif not comentario_aberto:
                linha_sem_comentarios += linha[i]
            i += 1

        if not comentario_aberto and linha_sem_comentarios.strip() != "":
            codigo_sem_comentarios.append(linha_sem_comentarios)

    return codigo_sem_comentarios

def include(line):
    included_files = []
    path = r"D:\MinGW\x86_64-w64-mingw32\include" #Colocar o caminho para a pasta com as bibliotecas
    line_divided = line.split()

    if line_divided and len(line_divided) >= 2 and line_divided[0] == '#include':
        file_name = line_divided[1].strip('"<>')
        path += '\\' + file_name

        if file_name not in included_files:
            included_files.append(file_name)

            with open(path, "r") as file:
                file_lines = file.readlines()

            included_content = ''.join(file_lines)
            return included_content

    return line

texto = removerComentarios(texto)

for i in range(0, len(texto)):

    if texto[i].startswith("#include"):
        texto[i] = include(texto[i])
        texto = removerComentarios(texto)
    elif texto[i].startswith("#define"):

        aux = ExpandirDefine(texto[i])
        index.append(i)
        
        for j in range(0, len(texto)):
             if aux[0] in texto[j]:
                 texto[j] = texto[j].replace(aux[0], aux[1])
  
    else:
        texto[i] = RemoverEspaços(texto[i])

for i in index:
    del(texto[i])

imprimir(texto)

with open("Resultado.c", "w") as arq:
    arq.write("".join(texto))
