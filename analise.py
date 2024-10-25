import pandas as pd

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
# Se as colunas forem separadas por vírgulas, use delimiter=','
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Verificar se as colunas "JI" e "TC" existem no DataFrame
if 'JI' in df.columns and 'TC' in df.columns:
    # Agrupar pela coluna "JI" e somar os valores da coluna "TC"
    agrupado = df.groupby('JI')['TC'].sum().reset_index()
    
    # Contar a quantidade de ocorrências de cada "JI"
    contagem_nomes = df['JI'].value_counts().reset_index()
    contagem_nomes.columns = ['JI', 'Quantidade']
    
    # Mesclar os DataFrames para obter a soma e a quantidade
    resultado = pd.merge(agrupado, contagem_nomes, on='JI')
    
    # Ordenar pela quantidade de "JI" em ordem decrescente
    resultado = resultado.sort_values(by='Quantidade', ascending=False)
    
    # Selecionar os top 10
    top_10 = resultado.head(10)
    
    # Exibir o resultado
    print(top_10)
else:
    print("As colunas 'JI' e/ou 'TC' não foram encontradas no arquivo.")