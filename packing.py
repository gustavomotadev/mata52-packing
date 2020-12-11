from copy import copy
from enum import IntEnum
from random import random
from sys import argv

try:
    from PIL import Image
    hasPIL = True
except ImportError:
    print("[AVISO] Voce nao possui o modulo PIL instalado, geracao e carregamento de imagens serao desabilitados!")
    hasPIL = False

#tipos de blocos
class TipoBloco(IntEnum):
    VAZIO = 0           #fora da area designada
    DISPONIVEL = 1      #disponivel para ser preenchido
    PREENCHIDO = 2      #ja preenchido
    BURACO = 3          #buraco que nao foi possivel de ser preenchido
    IMPOSSIVEL = 4      #buraco que não poderia ser preenchido de nenhuma maneira

#enumeracao dos percursos de varredura e boustrophedon a serem testados
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

#enumeracao dos percursos espirais a serem testados
#esperal descrescente foi removida por ser uma solucao ruim
enumEspirais = {
    0: (True, False, 0),
    1: (True, False, 1),
    2: (True, False, 2),
    3: (True, False, 3),
    4: (True, True, 0),
    5: (True, True, 1),
    6: (True, True, 2),
    7: (True, True, 3),
    #8: (False, False, 0),
    #9: (False, False, 1),
    #10: (False, False, 2),
    #11: (False, False, 3),
    #12: (False, True, 0),
    #13: (False, True, 1),
    #14: (False, True, 2),
    #15: (False, True, 3)
}

#dicionario utilitario com posicoes de celulas para funcoes
paridade_dict = {
    0: [(0, 0), (0, 1), (1, 0), (1, 1)],
    1: [(0, 0), (0, -1), (1, 0), (1, -1)],
    2: [(0, 0), (0, 1), (-1, 0), (-1, 1)],
    3: [(0, 0), (0, -1), (-1, 0), (-1, -1)]
}

#funcao utilitaria
#checa se uma coordenada esta dentro ou fora dos limites da matriz
def dentro(largura, altura, x, y):
    if x < 0 or y < 0 or not x < largura or not y < altura:
        return False
    else:
        return True

#funcao utilitaria para a funcao random_fill()
#assegura que a figura gerada se concentre no centro
#e cresca aleatoriamente até próximo das bordas
#modificar os pesos modifica o estilo de figura gerada
def nova_chance(x, y, largura):
    return (1 / (1 + ( ((x-(largura/2))/(largura/4))**2 + 
        ((y-(largura/2))/(largura/4))**2) ))*0.30 + random()*0.70

#implementacao iterativa de um algoritmo recursivo baseado no 
#flood fill porem com condicao de parada aleatoria
#gera figuras para serem usadas no problema
#as figuras se assemelham a "ilhas" porem com buracos
def random_fill(matriz, largura, valor, chance, iniX, iniY):
    
    X = 0
    Y = 1
    #a lista e usada como os proximos pontos a serem verificados
    #substituindo a caracteristica recursiva
    #manter a recursividade faria a pilha estourar em imagens largas
    lista = []
    lista.append((iniX, iniY))
    t = 1
    p = 0

    while p < t:

        #checar se deve preencher celula
        if (random() < nova_chance(lista[p][X], lista[p][Y], largura) and
            dentro(largura, largura, lista[p][X], lista[p][Y]) and 
            matriz[lista[p][Y]][lista[p][X]] != valor):
            
            #pintar celula
            matriz[lista[p][Y]][lista[p][X]] = valor
            
            #adicionar mais 4 celulas, equivalente a 4 chamadas recursivas
            t += 4
            lista.append((lista[p][X]-1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]-1))
            lista.append((lista[p][X]+1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]+1))
        
        p += 1

#implementacao do algoritmo bastante conhecido chamado flood fill
def flood_fill(matriz, largura, preencher, valor, iniX, iniY):
    
    X = 0
    Y = 1
    lista = []
    lista.append((iniX, iniY))
    t = 1
    p = 0

    while p < t:

        #checar se deve preencher celula
        if (dentro(largura, largura, lista[p][X], lista[p][Y]) and 
            matriz[lista[p][Y]][lista[p][X]] == preencher):

            #pintar a celula
            matriz[lista[p][Y]][lista[p][X]] = valor
            
            #adicionar mais 4 celulas, equivalente a 4 chamadas recursivas
            t += 4
            lista.append((lista[p][X]-1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]-1))
            lista.append((lista[p][X]+1, lista[p][Y]))
            lista.append((lista[p][X], lista[p][Y]+1))
        
        p += 1

#preenche todos as celulas iguais a um certo valor
#faz uma varredura completa da imagem e altera os valores
def fill_all(matriz, largura, preencher, valor):
    for i in range(largura):
        for j in range(largura):
            if matriz[j][i] == preencher:
                matriz[j][i] = valor

#funcao que executa os passos para gerar a imagem aleatoria
def matriz_aleatoria(largura):

    #cria matriz vazia
    matriz = [[0 for _ in range(largura)] for __ in range(largura)]

    #executa random_fill para gerar uma figura aleatoria
    random_fill(matriz, largura, 1, 1.0, largura//2, largura//2)
    #executa flood fill no exterior da figura para mante-lo intacto
    flood_fill(matriz, largura, 0, 4, 0, 0)
    #preenche os buracos da figura
    fill_all(matriz, largura, 0, 1)
    #retorna o exterior para seu estado devido com outro flood fill
    flood_fill(matriz, largura, 4, 0, 0, 0)

    return matriz

if hasPIL:
    #recupera um problema para resolver de um arquivo de imagem
    #qualquer pixel que não seja branco é considerado como fazendo parte da figura
    #branco é considerado o exterior
    def matriz_de_arquivo(nome):
        img_src = Image.open(nome).convert(mode='RGB')

        matrix = img_src.getdata()

        matriz = [[None for _ in range(img_src.width)] for __ in range(img_src.height)]

        for i in range(0, len(matrix), img_src.width):
            for j in range(img_src.width):
                matriz[i//img_src.width][j] = TipoBloco.VAZIO if matrix[i+j] == (255, 255, 255) else TipoBloco.DISPONIVEL

        return matriz, img_src.width, img_src.height

    #cria uma imagem do problema para visualização
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

#encontra a n-paridade de uma celula da matriz
def paridade(matriz, largura, altura, par, x, y):

    for celula in paridade_dict[par]:
        if (not dentro(largura, altura, celula[1]+x, celula[0]+y) or 
            matriz[celula[0]+y][celula[1]+x] != TipoBloco.DISPONIVEL):
            return False
    
    return True

#encontra quantas n-paridades uma celula possui
def num_paridades(matriz, largura, altura, x, y):
    soma = 0
    for par in range(4):
        if paridade(matriz, largura, altura, par, x, y):
            soma += 1
    return soma

#faz o processo de embutir um bloco 2x2 no local especificado
#so deve ser chamado apos checar que e possivel faze-lo
def preencher(matriz, par, x, y):
    for celula in paridade_dict[par]:
        matriz[celula[0]+y][celula[1]+x] = TipoBloco.PREENCHIDO

#funcao de visualizacao, gera um mapa de tons de vermelho, laranja e amarelo
#mostrando o numero de n-paridades de cada celula
def mapear_paridade(matriz, largura, altura):

    PAR_OFFSET = 6

    matriz_cp = copy(matriz)

    for y in range(altura):
        for x in range(largura):
            matriz[y][x] = num_paridades(matriz_cp, largura, altura, x, y) + PAR_OFFSET

#funcao de visualizacao
#usada para pintar os blocos impossiveis de rosa
def pintar_impossiveis(matriz, largura, altura):
    for y in range(altura):
        for x in range(largura):
            if (matriz[y][x] == TipoBloco.DISPONIVEL and 
                num_paridades(matriz, largura, altura, x, y) == 0):

                matriz[y][x] = TipoBloco.IMPOSSIVEL

#funcao de visualizacao
#serve para colocar a cor verde nos buracos
def pintar_buracos(matriz, largura, altura):
    for y in range(altura):
        for x in range(largura):
            if (matriz[y][x] == TipoBloco.DISPONIVEL and 
                num_paridades(matriz, largura, altura, x, y) == 0):
                matriz[y][x] = TipoBloco.BURACO

#essa funcao e utilizada para preencher e para simular o preenchimento de percursos
def preencher_percurso(matriz, largura, altura, percurso, par):
    soma = 0
    
    for point in percurso:
        if paridade(matriz, largura, altura, par, point[0], point[1]):
            preencher(matriz, par, point[0], point[1])
            soma += 1
    
    return soma

#funcao que gera os percursos de varredura e boustrophedon
#suas variaveis controlam as carcteristicas do percurso
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

#funcao utilitaria da funcao que gera percursos espirais
#serve para produzir segmentos da espiral em uma dada ordem
def parte_espiral(num, xMinMax, yMinMax):

    lista = []
    MIN = 0
    MAX = 1

    if num == 0:
        for x in range(xMinMax[MIN], xMinMax[MAX]):
            lista.append((x, yMinMax[MIN]))
    elif num == 1:
        for y in range(yMinMax[MIN], yMinMax[MAX]):
            lista.append((xMinMax[MAX], y))
    elif num == 2:
        for x in range(xMinMax[MAX], xMinMax[MIN], -1):
            lista.append((x, yMinMax[MAX]))
    elif num == 3:
        for y in range(yMinMax[MAX], yMinMax[MIN], -1):
            lista.append((xMinMax[MIN], y))

    return lista

#funcao que gera os percursos espirais a serem testados
#suas variaveis controlam as carcteristicas do percurso
#esse algoritmo e uma implementacao iterativa de um algoritmo recursivo
def percurso_espiral(xMinMax, yMinMax, invertido, sentido, ordem):
    
    lista = []
    MIN = 0
    MAX = 1
    _ordem = [0, 1, 2, 3]
    _ordem = _ordem[ordem:] + _ordem[:ordem]
    xMaxBackup = xMinMax[MAX]

    while xMinMax[MAX] > xMinMax[MIN] and yMinMax[MAX] > yMinMax[MIN]:

        for p in _ordem:
            lista.extend(parte_espiral(p, xMinMax, yMinMax))

        xMinMax[MIN] += 1
        xMinMax[MAX] -= 1
        yMinMax[MIN] += 1
        yMinMax[MAX] -= 1

    #caso base
    if xMinMax[MIN] == xMinMax[MAX] == yMinMax[MIN] == yMinMax[MAX]:
        #celula unica
        lista.append((xMinMax[MIN], xMinMax[MAX]))
    elif xMinMax[MIN] == xMinMax[MAX] or yMinMax[MIN] == yMinMax[MAX]:
        #linha/coluna
        lista.extend(parte_espiral(_ordem[0], xMinMax, yMinMax))
        lista.extend(parte_espiral(_ordem[2], xMinMax, yMinMax)[:1])
        lista.extend(parte_espiral(_ordem[1], xMinMax, yMinMax))
        lista.extend(parte_espiral(_ordem[3], xMinMax, yMinMax)[:1])

    if sentido:
        for i in range(len(lista)):
            lista[i] = (xMaxBackup-lista[i][0], lista[i][1])

    if invertido:
        lista = list(reversed(lista))

    return lista

#essa funcao meramente chama as outras funcoes de gerar cada tipo de percurso
#e os coloca juntos numa lista e os retorna
def gerarPercursos(rangeX, rangeY):
    listas = [None for _ in range(
        len(enumPercursos) + len(enumEspirais))]

    for i in range(len(enumPercursos)):
        listas[i] = gerarPercurso(
            enumPercursos[i][0], 
            enumPercursos[i][1], 
            enumPercursos[i][2],
            enumPercursos[i][3],
            rangeX, rangeY)

    for i in range(len(enumEspirais)):
        listas[i + len(enumPercursos)] = percurso_espiral(
            [rangeX[0], rangeX[-1]], 
            [rangeY[0], rangeY[-1]], 
            enumEspirais[i][0], 
            enumEspirais[i][1], 
            enumEspirais[i][2])

    return listas

#essa funcao simula o preenchimento em um dos percursos
#percorrendo as celulas da maneira especificada por ele e
#calculando quandos blocos seriam inseridos para cada
#n-paridade relevante. retorna esses valores ao final
def calcular_percurso(matriz, largura, altura, percurso):
    
    soma = [0, 0, 0, 0]

    matrizes = [[[None for _ in range(largura)] for __ in range(altura)] for ___ in range(4)]

    for p in range(4):
        for y in range(altura):
            for x in range(largura):
                matrizes[p][y][x] = int(matriz[y][x])
        
        soma[p] = preencher_percurso(matrizes[p], largura, altura, percurso, p)

    return soma

#essa funcao usa calcular_percurso() para descobrir qual dos percursos
#gerados e o melhor e deveria ser escolhido
def melhor_percurso(matriz, percursos, largura, altura):

    melhor_soma = [0, 0, 0, 0]
    melhor_paridade = 0
    melhor_percurso = []

    for percurso in percursos:
        soma = calcular_percurso(matriz, largura, altura, percurso)

        for p in range(4):
            if soma[p] > melhor_soma[melhor_paridade]:
                melhor_paridade = p
                melhor_soma = soma
                melhor_percurso = percurso

    return (melhor_percurso, 
        percursos.index(melhor_percurso), 
        melhor_paridade, 
        melhor_soma[melhor_paridade])

#funcao para gerar metricas para relatorio em texto
def borda(matriz, largura, altura, x, y):

    if (matriz[y][x] != TipoBloco.VAZIO and 
        (x == 0 or y == 0 or x == largura-1 or y == altura-1 or
        matriz[y][x-1] == TipoBloco.VAZIO or 
        matriz[y][x+1] == TipoBloco.VAZIO or 
        matriz[y-1][x] == TipoBloco.VAZIO or 
        matriz[y+1][x] == TipoBloco.VAZIO)): 

        return True
    
    return False

#funcao utilizada para gerar relatorios sobre as quantidades de cada
#bloco ou caracteristica relevante da solucao
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

#funcao que formata e imprime o relatorio informativo
def gerar_relatorio(quantidades, largura, altura, tipo, embutidos):
    
    print('Blocos 2x2 embutidos: ' + str(embutidos))
    print('Tipo da solucao: ', end='')
    if tipo < 8:
        print('Varredura ' + str(tipo))
    elif tipo < 16:
        print('Boustrophedon ' + str(tipo - 8))
    elif tipo < 24:
        print('Espiral Crescente ' + str(tipo - 16))
    #elif tipo < 32:
        #print('Espiral Decrescente ' + str(tipo - 24))
    print('Largura x Altura: ' + str(largura) + ' x ' + str(altura) + ' = ' + str(largura*altura))
    print('Celulas nao vazias: ' + str(quantidades[2]+quantidades[3]+quantidades[4]) + ' = {Preenchidas: ' + str(quantidades[2]) + 
        '; Buracos: ' + str(quantidades[3]) + '; Impossiveis: ' + str(quantidades[4]) + '}')
    try:
        print('% Possiveis preenchidas: ' + str(round((quantidades[2]/(quantidades[2]+quantidades[3]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass
    try:
        print('% Interior preenchido: ' + str(round((quantidades[5]/(quantidades[6]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass
    try:
        print('% Borda preenchida: ' + str(round((quantidades[7]/(quantidades[8]) * 100), 2)) + '%')
    except ZeroDivisionError:
        pass

#funcao que corta a imagem deixando apenas a porcao relevante para o problema
def crop(matriz, largura, altura):
    minX = minY = 999999
    maxX = maxY = 0

    for y in range(altura):
        for x in range(largura):
            if matriz[y][x] != TipoBloco.VAZIO:

                if x < minX:
                    minX = x
                elif x > maxX:
                    maxX = x

                if y < minY:
                    minY = y
                elif y > maxY:
                    maxY = y

    nova_largura = maxX - minX + 1
    nova_altura = maxY - minY + 1
    nova_matriz = [[None for _ in range(nova_largura)] for __ in range(nova_altura)]

    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            nova_matriz[y - minY][x - minX] = matriz[y][x]
    
    return nova_matriz, nova_largura, nova_altura

#funcao facilitadora que refaz o processo de gerar imagem aleatoria
#garantindo os limites desejados e o recorte apropriado da matriz
def matriz_aleatoria_limitada(minL, maxL):
    largura = altura = maxL
    matriz = matriz_aleatoria(largura)
    matriz, largura, altura = crop(matriz, largura, altura)
    while largura < minL or altura < minL:
        largura = altura = maxL
        matriz = matriz_aleatoria(largura)
        matriz, largura, altura = crop(matriz, largura, altura)
    
    return matriz, largura, altura

######################################################################################

def main():

    if len(argv) == 3:
        try:
            minimo = int(argv[1])
            maximo = int(argv[2])
        except:
            minimo = 16
            maximo = 64

    #usar para obter problema de arquivo, apenas se tiver o modulo PIL
    #matriz, largura, altura = matriz_de_arquivo('..nome_do_arquivo.png')

    matriz, largura, altura = matriz_aleatoria_limitada(minimo, maximo)

    pintar_impossiveis(matriz, largura, altura)
    percursos = gerarPercursos(range(largura), range(altura))
    percurso, tipo, paridade, embutidos = melhor_percurso(matriz, percursos, largura, altura)
    preencher_percurso(matriz, largura, altura, percurso, paridade)
    pintar_buracos(matriz, largura, altura)

    gerar_relatorio(quantidade_blocos(matriz, largura, altura), largura, altura, tipo, embutidos)

    if hasPIL:
        matriz_para_imagem(matriz, largura, altura, 8, True).show()

if __name__ == "__main__":
    main()