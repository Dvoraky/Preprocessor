import os, sys, re

for Y in range(1, len(sys.argv)):

    cwd = os.getcwd()
    path = sys.argv[Y]
    path = cwd + "\\" + path

    texto = []
    index = []

    with open(path, "r") as arquivo:
        texto = arquivo.readlines()

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
        aux = linha.split()
        variavel = aux[1]
        parametros = ', '.join(aux[2:]).replace('(', '').replace(')', '')  # Obtém os parâmetros sem parênteses
        valor = f'({parametros})'  # Formata os parâmetros entre parênteses

        return variavel, valor


    def DefineMacro(linha):
        partes = re.findall(r'\w+|\([^()]*\)|\S+', linha)
        partes_sem_parenteses = [parte.strip('()') for parte in partes]
        nome_macro = partes_sem_parenteses[1]
        parametros = partes_sem_parenteses[2].strip(',').replace(',', '')
        parametros = parametros.split()

        operadores = ['+', '-', '*', '/', '=']

        indice_operador = next((indice for indice, parte in enumerate(partes_sem_parenteses) if parte in operadores), None)

        operador_define = partes_sem_parenteses[indice_operador] if indice_operador is not None else ""

        return nome_macro, operador_define


    def removerComentarios(texto):
        codigo_sem_comentarios = []
        comentario_aberto = False

        for linha in texto:
            linha_sem_comentarios = ""

            i = 0
            while i < len(linha):
                if not comentario_aberto and linha[i:i + 2] == "//":
                    break
                elif not comentario_aberto and linha[i:i + 2] == "/*":
                    comentario_aberto = True
                    i += 2
                    continue
                elif comentario_aberto and linha[i:i + 2] == "*/":
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
        path = r"D:\MinGW\x86_64-w64-mingw32\include" #Trocar pelo path de onde se encontra as bibliotecas no seu computador
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

    # Verifica se uma linha está marcada para exclusão
    def linha_para_excluir(linha):
        for i in index:
            if linha.startswith(texto[i]):
                return True
        return False
    indice = []
    for i in range(len(texto)):
        if linha_para_excluir(texto[i]):
            continue

        if texto[i].startswith("#include"):
            indice.append(i)
            
        elif texto[i].startswith("#define"):
            if '(' in texto[i]:
                index.append(i)
                auxiliar = DefineMacro(texto[i])
                nome_macro = auxiliar[0]
                operador_define = auxiliar[1]

                for j in range(len(texto)):
                    if nome_macro in texto[j]:
                        pattern = re.compile(rf'{nome_macro}\((.*?)\)', re.DOTALL)
                        match = pattern.search(texto[j])
                        if match:
                            parametros_str = match.group(1)
                            novo_parametros_str = parametros_str.replace(',', f' {operador_define} ')
                            texto[j] = pattern.sub(f'{nome_macro}({novo_parametros_str})', texto[j])
                            texto[j] = texto[j].replace(nome_macro, '')

            else:
                aux = ExpandirDefine(texto[i])
                index.append(i)

                for j in range(len(texto)):
                    if aux[0] in texto[j]:
                        texto[j] = texto[j].replace(aux[0], aux[1])

        else:
            texto[i] = RemoverEspaços(texto[i])
            
    for i in indice:
        texto[i] = include(texto[i])


    codigo_final = []
    for i in range(len(texto)):
        if not linha_para_excluir(texto[i]):
            codigo_final.append(texto[i])

    texto = codigo_final

    nome_arquivo = "Resultado" + str(Y) + ".c"
    with open(nome_arquivo, "w") as arq:
        arq.write("".join(texto))
