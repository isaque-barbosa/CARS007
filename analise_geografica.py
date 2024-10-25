import pandas as pd
import geopandas as gpd
import folium
from geopy.geocoders import Nominatim

# Caminho do arquivo TXT que você deseja abrir
caminho_arquivo = './novo_trabalho/concatenado.txt'

# Ler o arquivo TXT como um DataFrame, assumindo que as colunas são separadas por tabulações
df = pd.read_csv(caminho_arquivo, delimiter='\t')

# Extrair as localizações das instituições
instituicoes = df['C1'].str.extract(r'\[(.*?)\]')
instituicoes = instituicoes.dropna().reset_index(drop=True)

# Usar o Nominatim para obter as coordenadas geográficas
geolocator = Nominatim(user_agent="research_cooccurrence")

def get_location(address):
    try:
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    except:
        return None

# Obter as coordenadas para cada instituição
coordenadas = []
for address in instituicoes[0]:
    coord = get_location(address)
    coordenadas.append(coord)

coordenadas = pd.Series(coordenadas).dropna().reset_index(drop=True)

# Criar um GeoDataFrame com as coordenadas
gdf = gpd.GeoDataFrame(coordenadas, geometry=gpd.points_from_xy([coord[1] for coord in coordenadas], [coord[0] for coord in coordenadas]))

# Carregar o arquivo 'naturalearth_lowres' localmente
world = gpd.read_file('./ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

# Criar um mapa usando Folium
m = folium.Map(location=[20, 0], zoom_start=2)

# Adicionar marcadores para cada localização
for idx, row in gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x]).add_to(m)

# Salvar o mapa como um arquivo HTML na pasta 'mapas'
m.save('./research_cooccurrence_map.html')

# Exibir o mapa (opcional)
# m