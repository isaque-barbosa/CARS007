import pandas as pd

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Verificar se as colunas "PY" e "DE" existem no DataFrame
if 'PY' in df.columns and 'DE' in df.columns:
    # Dividir as keywords em listas
    df['DE'] = df['DE'].str.split(';')
    
    # Explodir as listas de keywords em linhas individuais
    df_exploded = df.explode('DE')
    
    # Limpar espaços em branco e converter para minúsculas
    df_exploded['DE'] = df_exploded['DE'].str.strip().str.lower()
    
    # Agrupar por ano e keyword, e contar a frequência
    resultado = df_exploded.groupby(['PY', 'DE']).size().reset_index(name='Quantidade')
    
    # Renomear as colunas para melhor legibilidade
    resultado.columns = ['Ano', 'Keyword', 'Quantidade']
    
    # Ordenar pelo ano e pela quantidade de keywords
    resultado = resultado.sort_values(by=['Ano', 'Quantidade'], ascending=[True, False])
    
    # Exibir o resultado
    print(resultado)

    # Salvar o resultado em um arquivo TXT
    resultado.to_csv('./keyword_per_year.txt', sep='\t', index=False)
else:
    print("As colunas 'PY' e/ou 'DE' não foram encontradas no arquivo.")