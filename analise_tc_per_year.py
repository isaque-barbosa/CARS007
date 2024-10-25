import pandas as pd

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Verificar se as colunas "PY" e "TC" existem no DataFrame
if 'PY' in df.columns and 'TC' in df.columns:
    # Contar o número de publicações por ano
    publicacoes_por_ano = df['PY'].value_counts().reset_index()
    publicacoes_por_ano.columns = ['Ano', 'Publicações']
    
    # Agrupar por ano e somar as citações
    citacoes_por_ano = df.groupby('PY')['TC'].sum().reset_index()
    citacoes_por_ano.columns = ['Ano', 'Citações']
    
    # Mesclar os DataFrames para obter o número de publicações e citações por ano
    resultado = pd.merge(publicacoes_por_ano, citacoes_por_ano, on='Ano')
    
    # Ordenar pelo ano
    resultado = resultado.sort_values(by='Ano')
    
    # Exibir o resultado
    print(resultado)
else:
    print("As colunas 'PY' e/ou 'TC' não foram encontradas no arquivo.")

# Usar Matplotlib para plotar gráficos