import pandas as pd
import re

# Carregar a base de dados (substitua 'sua_base_de_dados.csv' pelo caminho do seu arquivo)
df = pd.read_csv('./novo_trabalho/concatenado.txt', delimiter='\t')

# Função para extrair o país da coluna 'C1'
def extract_country(institution_info):
    if pd.isna(institution_info):
        return None
    match = re.search(r'PL-\d+', institution_info)
    if match:
        return 'Poland'
    match = re.search(r'CH-\d+', institution_info)
    if match:
        return 'Switzerland'
    # Adicione outras regras para outros países conforme necessário
    return None

# Extrair o primeiro autor e o país
df['First_Author'] = df['AU'].str.split(';').str[0]
df['Country'] = df['C1'].apply(extract_country)

# Agrupar por autor e país, contando o número de publicações
author_country_group = df.groupby(['First_Author', 'Country']).size().reset_index(name='Publication_Count')

# Ordenar pelo número de publicações em ordem decrescente
author_country_group = author_country_group.sort_values(by='Publication_Count', ascending=False)

# Pegar os top 100 autores
top_100_authors = author_country_group.head(100)

# Exibir o resultado
print(top_100_authors)

# Salvar o resultado em um arquivo CSV (opcional)
top_100_authors.to_csv('top_100_authors.csv', index=False)