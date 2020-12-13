import pandas as pd
import matplotlib.pyplot as plt

dados = pd.read_csv('dados.csv', ';', header=0)

dados = dados[dados.tipo != 'Espiral Decrescente ']

print('--- Quantidade de Dados ---')
print(len(dados))

minimos = dados.min()
maximos = dados.max()
medias = dados.mean()
medianas = dados.median()
desvios = dados.std()
minimos.pop('tipo')
maximos.pop('tipo')

print('--- Mínimos ---')
print(minimos)
print('--- Máximos ---')
print(maximos)
print('--- Médias ---')
print(medias)
print('--- Medianas ---')
print(medianas)
print('--- Desvios ---')
print(desvios)

frequencia_tipos = dados['tipo'].value_counts()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
fig.suptitle('Porcentagem de Área Preenchida por Região')
dados.boxplot(column=[r'%possiveis'], ax=ax1)
dados.boxplot(column=[r'%interior'], ax=ax2)
dados.boxplot(column=[r'%borda'], ax=ax3)
ax1_range = [85+x*1.25 for x in range(13)]
ax2_range = [94+x*0.5 for x in range(13)]
ax3_range = range(45, 100+1, 5)
ax1.set_yticks(ticks=ax1_range)
ax2.set_yticks(ticks=ax2_range)
ax3.set_yticks(ticks=ax3_range)
ax1.set_yticklabels(labels=map(lambda x: str(x)+'%', ax1_range))
ax2.set_yticklabels(labels=map(lambda x: str(x)+'%', ax2_range))
ax3.set_yticklabels(labels=map(lambda x: str(x)+'%', ax3_range))
ax1.set_xticklabels(labels=['Possível'])
ax2.set_xticklabels(labels=['Interior'])
ax3.set_xticklabels(labels=['Borda'])
plt.subplots_adjust(wspace=0.7)
plt.show()

plt.figure()
plt.title("Porcentagem de Problemas Resolvidos por Classe")
plt.pie(x=list(frequencia_tipos), explode=[0.01, 0.01, 0.01], 
    autopct=lambda x: str(round(x,2))+'%', 
    textprops={'color': 'black', 'weight': 'bold'},
    colors=['steelblue', 'deepskyblue', 'lightskyblue'],
    labels=['Boustrophedon', 'Varredura', 'Espiral'])
plt.show()