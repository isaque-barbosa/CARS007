import pandas as pd

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Verificar se as colunas "TI" e "TC" existem no DataFrame
if 'TI' in df.columns and 'TC' in df.columns and 'PY' in df.columns:
    # Agrupar pela coluna "TI" e somar os valores da coluna "TC"
    agrupado = df.groupby('TI')['TC'].sum().reset_index()
    
    # Contar a quantidade de ocorrências de cada "TI"
    contagem_nomes = df['TI'].value_counts().reset_index()
    contagem_nomes.columns = ['TI', 'Quantidade']
    
    # Mesclar os DataFrames para obter a soma e a quantidade
    resultado = pd.merge(agrupado, contagem_nomes, on='TI')
    
    # Ordenar pela quantidade de "TC" em ordem decrescente
    resultado = resultado.sort_values(by='TC', ascending=False)
    
    # Selecionar os top 10
    top_10 = resultado.head(10)
    
    # Adicionar a coluna de média de citações por ano
    top_10['Media_Citações_por_Ano'] = top_10['TC'] / (2024 - df[df['TI'].isin(top_10['TI'])]['PY'].values)
    
    # Exibir o resultado
    print(top_10)
else:
    print("As colunas 'TI', 'TC' e/ou 'PY' não foram encontradas no arquivo.")