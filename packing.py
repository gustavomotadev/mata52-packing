from enum import IntEnum
from PIL import Image
from copy import copy, deepcopy
from random import random, shuffle

class TipoBloco(IntEnum):
    VAZIO = 0
    DISPONIVEL = 1
    PREENCHIDO = 2
    BURACO = 3
    IMPOSSIVEL = 4

enumPercursos = {
    0: (False, False, False, False),
    1: (False, False, False, True),
    2: (False, False, True, False),
    3: (False, False, True, True),
    4: (False, True, False, False),
    5: (False, True, False, True),
    6: (False, True, True, False),
    7: (False, True, True, True),
    8: (True, False, False, False),
    9: (True, False, False, True),
    10: (True, False, True, False),
    11: (True, False, True, True),
    12: (True, True, False, False),
    13: (True, True, False, True),
    14: (True, True, True, False),
    15: (True, True, True, True)
}

def nova_chance(x, y, largura):
    if x == int(largura/2)  and y == int(largura/2):
        return 1
    else:
        return (1 / (1 + ( ((x-(largura/2))/(largura/4))**2 + ((y-(largura/2))/(largura/4))**2) ))*0.30 + random()*0.70

def random_fill(matriz, largura, valor, chance, iniX, iniY):
    
    X = 0
    Y = 1
    lista = []
    lista.append((iniX, iniY))
    t = 1
    p = 0

    while p < t:

        if (random() < nova_chance(lista[p][X], lista[p][Y], largura) and
            lista[p][X] > 0 and lista[p][X] < largura and 
            lista[p][Y] > 0 and lista[p][Y] < largura and 
            matriz[lista[p][Y]][lista[p][X]] != valor):

            matriz[lista[p][Y]][lista[p][X]] = valor
            t += 4
            lista.append((lista[p][X]-1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]-1))
            lista.append((lista[p][X]+1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]+1))
        
        p += 1

def flood_fill(matriz, largura, preencher, valor, iniX, iniY):
    
    X = 0
    Y = 1
    lista = []
    lista.append((iniX, iniY))
    t = 1
    p = 0

    while p < t:

        if (lista[p][X] >= 0 and lista[p][X] < largura and 
            lista[p][Y] >= 0 and lista[p][Y] < largura and 
            matriz[lista[p][Y]][lista[p][X]] == preencher):

            matriz[lista[p][Y]][lista[p][X]] = valor
            t += 4
            lista.append((lista[p][X]-1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]-1))
            lista.append((lista[p][X]+1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]+1))
        
        p += 1

def fill_all(matriz, largura, preencher, valor):
    for i in range(largura):
        for j in range(largura):
            if matriz[j][i] == preencher:
                matriz[j][i] = valor

def matriz_aleatoria(largura):

    matriz = [[0 for _ in range(largura)] for __ in range(largura)]

    random_fill(matriz, largura, 1, 1.0, largura//2, largura//2)
    flood_fill(matriz, largura, 0, 4, 0, 0)
    fill_all(matriz, largura, 0, 1)
    flood_fill(matriz, largura, 4, 0, 0, 0)

    return matriz


def matriz_de_arquivo(nome):
    img_src = Image.open(nome).convert(mode='RGB')

    matrix = img_src.getdata()

    matriz = [[None for _ in range(img_src.width)] for __ in range(img_src.height)]

    for i in range(0, len(matrix), img_src.width):
        for j in range(img_src.width):
            matriz[i//img_src.width][j] = TipoBloco.VAZIO if matrix[i+j] == (255, 255, 255) else TipoBloco.DISPONIVEL

    return matriz, img_src.width, img_src.height

def matriz_para_imagem(matriz, largura, altura, fator, grade):

    if grade:
        correcao = 1
    else:
        correcao = 0
    fator = fator + correcao

    lista_cores = [(255, 255, 255), (127, 127, 127), (16, 16, 192), 
        (16, 192, 16), (192, 16, 192), (0, 255, 255), (127, 0, 0), 
        (255, 64, 0), (255, 128, 0), (255, 192, 0), (255, 255, 0)]
    paleta = [lista_cores[i][j] if i < len(lista_cores) else 0 
        for i in range(256) for j in range(3)]

    img_dest = Image.new('P', (largura*fator + correcao, altura*fator + correcao), 
        color=TipoBloco.VAZIO)
    img_dest.putpalette(paleta)
    pixels = img_dest.load()

    if grade:
        for i in range(altura*fator + correcao):
            for j in range(largura*fator + correcao):
                if i % fator == 0 or j % fator == 0:
                    pixels[j,i] = 255
                else:
                    pixels[j,i] = matriz[i//fator][j//fator]
    else:
        for i in range(altura*fator):
            for j in range(largura*fator):
                pixels[j,i] = matriz[i//fator][j//fator]

    return img_dest

def dentro(matriz, largura, altura, x, y):
    if x < 0 or y < 0 or not x < largura or not y < altura:
        return False
    else:
        return True

def paridade(matriz, largura, altura, par, x, y):
    lista = []

    if par == 0:
        lista.extend([(y, x), (y, x+1), (y+1, x), (y+1, x+1)])
    elif par == 1:
        lista.extend([(y, x), (y, x-1), (y+1, x-1), (y+1, x)])
    elif par == 2:
        lista.extend([(y, x), (y, x+1), (y-1, x), (y-1, x+1)])
    elif par == 3:
        lista.extend([(y, x), (y, x-1), (y-1, x), (y-1, x-1)])

    #print(lista)
    for celula in lista:
        if (not dentro(matriz, largura, altura, celula[1], celula[0]) or 
            matriz[celula[0]][celula[1]] != TipoBloco.DISPONIVEL):
            return False
    
    return True

def num_paridades(matriz, largura, altura, x, y):
    sum = 0
    for par in range(4):
        if paridade(matriz, largura, altura, par, x, y):
            sum += 1
    return sum

def preencher(matriz, par, x, y):
    if par == 0:
        matriz[y][x] = TipoBloco.PREENCHIDO
        matriz[y][x+1] = TipoBloco.PREENCHIDO
        matriz[y+1][x] = TipoBloco.PREENCHIDO
        matriz[y+1][x+1] = TipoBloco.PREENCHIDO
    elif par == 1:
        matriz[y][x] = TipoBloco.PREENCHIDO
        matriz[y][x-1] = TipoBloco.PREENCHIDO
        matriz[y+1][x-1] = TipoBloco.PREENCHIDO
        matriz[y+1][x] = TipoBloco.PREENCHIDO
    elif par == 2:
        matriz[y][x] = TipoBloco.PREENCHIDO
        matriz[y][x+1] = TipoBloco.PREENCHIDO
        matriz[y-1][x] = TipoBloco.PREENCHIDO
        matriz[y-1][x+1] = TipoBloco.PREENCHIDO
    elif par == 3:
        matriz[y][x] = TipoBloco.PREENCHIDO
        matriz[y][x-1] = TipoBloco.PREENCHIDO
        matriz[y-1][x] = TipoBloco.PREENCHIDO
        matriz[y-1][x-1] = TipoBloco.PREENCHIDO

def preencher_paridade(matriz, largura, altura, par):
    soma = 0
    for y in range(altura):
        for x in range(largura):
            if paridade(matriz, largura, altura, par, x, y):
                preencher(matriz, par, x, y)
                soma += 1
    #print(soma)

def mapear_paridade(matriz, largura, altura):

    PAR_OFFSET = 6

    matriz_cp = copy(matriz)

    for y in range(altura):
        for x in range(largura):
            matriz[y][x] = num_paridades(matriz_cp, largura, altura, x, y) + PAR_OFFSET

def pintar_buracos(matriz, largura, altura):
    for y in range(altura):
        for x in range(largura):
            if (matriz[y][x] == TipoBloco.DISPONIVEL and 
                num_paridades(matriz, largura, altura, x, y) == 0):
                matriz[y][x] = TipoBloco.BURACO

def gerarPercurso(bpd, startOnX, invX, invY, rangeX, rangeY):
    lista = []
    rangeX = list(reversed(rangeX)) if invX else rangeX
    rangeY = list(reversed(rangeY)) if invY else rangeY
    rangeA = rangeX if startOnX else rangeY
    rangeB = rangeY if startOnX else rangeX

    for a in rangeA:
        for b in rangeB:
            lista.append((a, b) if startOnX else (b, a))
        if bpd:
            rangeB = list(reversed(rangeB))
    return lista

def gerarPercursos(rangeX, rangeY):
    listas = [None for _ in range(len(enumPercursos))]

    for i in range(len(enumPercursos)):
        listas[i] = gerarPercurso(enumPercursos[i][0], 
            enumPercursos[i][1], 
            enumPercursos[i][2],
            enumPercursos[i][3],
            rangeX, rangeY)

    return listas

def calcular_percurso(matriz, largura, altura, percurso):
    
    soma = [0, 0, 0, 0, 0]

    matrizes = [[[None for _ in range(largura)] for __ in range(altura)] for ___ in range(5)]

    for p in range(5):
        for y in range(altura):
            for x in range(largura):
                matrizes[p][y][x] = int(matriz[y][x])
        
        soma[p] = preencher_percurso(matrizes[p], largura, altura, percurso, p)

    print(soma)
    return soma

def melhor_percurso(matriz, percursos, largura, altura):

    melhor_soma = [0, 0, 0, 0, 0]
    melhor_paridade = 0
    melhor_percurso = []

    for percurso in percursos:
        soma = calcular_percurso(matriz, largura, altura, percurso)

        for p in range(5):
            if soma[p] > melhor_soma[melhor_paridade]:
                melhor_paridade = p
                melhor_soma = soma
                melhor_percurso = percurso

    print((melhor_paridade, melhor_soma[melhor_paridade]))

    return melhor_percurso, melhor_paridade

def preencher_percurso(matriz, largura, altura, percurso, par):
    soma = 0
    if par == 4:
        for point in percurso:
            rangeP = list(range(4))
            shuffle(rangeP)
            for p in rangeP:
                if paridade(matriz, largura, altura, p, point[0], point[1]):
                    preencher(matriz, p, point[0], point[1])
                    soma += 1
    else:
        for point in percurso:
            if paridade(matriz, largura, altura, par, point[0], point[1]):
                preencher(matriz, par, point[0], point[1])
                soma += 1
    
    return soma

def pintar_impossiveis(matriz, largura, altura):
    for y in range(altura):
        for x in range(largura):
            if (matriz[y][x] == TipoBloco.DISPONIVEL and 
                num_paridades(matriz, largura, altura, x, y) == 0):

                matriz[y][x] = TipoBloco.IMPOSSIVEL

def borda(matriz, largura, altura, x, y):

    if (matriz[y][x] != TipoBloco.VAZIO and 
        (x == 0 or y == 0 or x == largura-1 or y == altura-1 or
        matriz[y][x-1] == TipoBloco.VAZIO or 
        matriz[y][x+1] == TipoBloco.VAZIO or 
        matriz[y-1][x] == TipoBloco.VAZIO or 
        matriz[y+1][x] == TipoBloco.VAZIO)): 

        return True
    
    return False

def pintar_borda(matriz, largura, altura):
    for y in range(altura):
        for x in range(largura):
            if borda(matriz, largura, altura, x, y):

                matriz[y][x] = 5

def quantidade_blocos(matriz, largura, altura):
    soma = [0 for _ in range(len(TipoBloco) + 4)]

    for y in range(altura):
        for x in range(largura):
            soma[matriz[y][x]] += 1

            if not matriz[y][x] == TipoBloco.VAZIO:
                if not borda(matriz, largura, altura, x, y):
                    soma[6] += 1
                    if matriz[y][x] == TipoBloco.PREENCHIDO:
                        soma[5] += 1
                else:
                    soma[8] += 1
                    if matriz[y][x] == TipoBloco.PREENCHIDO:
                        soma[7] += 1
                

    return soma

def gerar_relatorio(quantidades):
    print('Nao Vazios: ' + str(quantidades[2]+quantidades[3]+quantidades[4]) + ' = {Preenchidos: ' + str(quantidades[2]) + 
        '; Buracos: ' + str(quantidades[3]) + '; Impossiveis: ' + str(quantidades[4]) + '}')
    try:
        print('% Possiveis Preenchidos: ' + str(round((quantidades[2]/(quantidades[2]+quantidades[3]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass
    try:
        print('% Interior Preenchido: ' + str(round((quantidades[5]/(quantidades[6]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass
    try:
        print('% Borda Preenchida: ' + str(round((quantidades[7]/(quantidades[8]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass

######################################################################################

def main():

    #matriz, largura, altura = matriz_de_arquivo('../imagens/32_0.png')

    largura = altura = 64
    matriz = matriz_aleatoria(largura)

    pintar_impossiveis(matriz, largura, altura)
    percursos = gerarPercursos(range(largura), range(altura))
    percurso, paridade = melhor_percurso(matriz, percursos, largura, altura)
    preencher_percurso(matriz, largura, altura, percurso, paridade)
    pintar_buracos(matriz, largura, altura)

    gerar_relatorio(quantidade_blocos(matriz, largura, altura))

    matriz_para_imagem(matriz, largura, altura, 8, False).show()


if __name__ == "__main__":
    main()