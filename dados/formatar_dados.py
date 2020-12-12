import re

PADRAO = re.compile(r'''Blocos 2x2 embutidos: ([0-9]+)
Tipo da solucao: ([a-zA-Z]+ [a-zA-Z]* ?)[0-9]
Largura x Altura: ([0-9]+) x ([0-9]+) = ([0-9]+)
Celulas nao vazias: ([0-9]+) = {Preenchidas: ([0-9]+); Buracos: ([0-9]+); Impossiveis: ([0-9]+)}
% Possiveis preenchidas: ([0-9]+.[0-9]+)%
% Interior preenchido: ([0-9]+.[0-9]+)%
% Borda preenchida: ([0-9]+.[0-9]+)%''', re.MULTILINE)

with open('dados.txt', 'r') as arquivo:
    dados = arquivo.readlines()

dados = [[dados[i], dados[i+1], dados[i+2], dados[i+3], dados[i+4], 
    dados[i+5], dados[i+6]] for i in range(0, len(dados), 7)]

dados = list(map(lambda x: ''.join(x), dados))

dados = list(map(lambda x: re.search(PADRAO, x).groups(), dados))

with open('dados.csv', 'w') as saida:
    saida.write(r'embutidos;tipo;largura;altura;tamanho;nao_vazias;preenchidas;buracos;impossiveis;%possiveis;%interior;%borda'+'\n')
    saida.writelines(list(map(lambda x: ';'.join(x) + '\n', dados)))