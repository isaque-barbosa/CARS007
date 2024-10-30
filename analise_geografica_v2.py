import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import re
import time

# Função para processar a coluna C1 e extrair as localizações das instituições
def extrair_localizacoes(texto):
    if pd.isna(texto):
        return []
    # Regex para remover o conteúdo entre colchetes e separar por ponto e vírgula
    regex = r'\[.*?\]|\s*;\s*'
    print(texto)
    
    # Substitui o conteúdo entre colchetes por uma string vazia e separa por ponto e vírgula
    resultados = re.split(regex, texto)
    
    # Remove strings vazias resultantes da separação
    resultados = [resultado.strip() for resultado in resultados if resultado.strip()]
    
    return resultados

# Função para obter as coordenadas geográficas de um endereço com retentativa e múltiplos serviços
def get_location(address, geolocators, max_retries=3, delay=2):
    for geolocator in geolocators:
        for attempt in range(max_retries):
            try:
                location = geolocator.geocode(address)
                if location is not None:
                    return (location.latitude, location.longitude)
                else:
                    print(f"Localização não encontrada para {address} usando {geolocator.__class__.__name__}")
                    break
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                else:
                    print(f"Erro ao geocodificar {address} usando {geolocator.__class__.__name__}: {e}")
                    break
            except Exception as e:
                print(f"Erro ao geocodificar {address} usando {geolocator.__class__.__name__}: {e}")
                break
    return None

# Função para criar o mapa com as localizações
def criar_mapa(coordenadas):
    # Criar um GeoDataFrame com as coordenadas
    gdf = gpd.GeoDataFrame(coordenadas, geometry=gpd.points_from_xy([coord[1] for coord in coordenadas], [coord[0] for coord in coordenadas]))

    # Carregar o arquivo 'naturalearth_lowres' localmente
    gpd.read_file('./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

    # Criar um mapa usando Folium
    m = folium.Map(location=[20, 0], zoom_start=2)

    # Adicionar marcadores para cada localização
    for _, row in gdf.iterrows():
        folium.Marker([row.geometry.y, row.geometry.x]).add_to(m)

    # Salvar o mapa como um arquivo HTML
    m.save('./research_cooccurrence_map.html')

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Converter a coluna C1 para strings e tratar valores ausentes
df['C1'] = df['C1'].astype(str)

# Extrair as localizações das instituições
df['Localizacoes'] = df['C1'].apply(extrair_localizacoes)

# Usar múltiplos serviços de geocodificação
geolocators = [
    Nominatim(user_agent="research_cooccurrence"),
    GoogleV3(api_key='SUA_API_KEY_DA_GOOGLE')
]

# Obter as coordenadas para cada instituição
coordenadas = []
for localizacoes in df['Localizacoes']:
    for address in localizacoes:
        coord = get_location(address, geolocators)
        if coord:
            coordenadas.append(coord)

# Remover coordenadas nulas
coordenadas = [coord for coord in coordenadas if coord is not None]

# Criar o mapa com as coordenadas
criar_mapa(coordenadas)