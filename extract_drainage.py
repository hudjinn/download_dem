import os
import gdal
import requests
import re
import json
import whitebox
from whitebox.whitebox_tools import WhiteboxTools
import geopandas as gpd

# Inicialização do WhiteboxTools
wbt = WhiteboxTools()

# Diretórios
input_dir = "downloaded"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Verificar se um arquivo é um DEM válido
def is_valid_dem(filepath):
    try:
        dataset = gdal.Open(filepath)
        if dataset is None:
            return False
        band = dataset.GetRasterBand(1)
        if band is None:
            return False
        return True
    except:
        return False


# Função para adicionar elevação ao GeoDataFrame
def add_elevation_to_gdf(gdf, dem_band, dem_dataset):
    def get_elevation(x, y):
        gt = dem_dataset.GetGeoTransform()
        inv_gt = gdal.InvGeoTransform(gt)
        px, py = gdal.ApplyGeoTransform(inv_gt, x, y)
        px, py = int(px), int(py)
        if 0 <= px < dem_band.XSize and 0 <= py < dem_band.YSize:
            elevation = dem_band.ReadAsArray(px, py, 1, 1)[0, 0]
            return elevation
        else:
            return None
    
    elevations = []
    for geom in gdf.geometry:
        if geom.geom_type == 'LineString':
            z_values = [get_elevation(x, y) for x, y in geom.coords]
            elevations.append(z_values)
        elif geom.geom_type == 'MultiLineString':
            z_values_multi = []
            for line in geom:
                z_values_multi.append([get_elevation(x, y) for x, y in line.coords])
            elevations.append(z_values_multi)
    return elevations

# Função principal
def main():
    # Verificar se há arquivos .tif no diretório de entrada
    tifs = [f for f in os.listdir(input_dir) if f.endswith('.tif')]
    if not tifs:
        print("No .tif files found in the input directory.")
        return
    
    # Verificar se algum arquivo .tif é um DEM válido
    valid_dem = None
    for tif in tifs:
        filepath = os.path.join(input_dir, tif)
        if is_valid_dem(filepath):
            valid_dem = filepath
            break
    
    if not valid_dem:
        print("No valid DEM files found in the input directory.")
        return
    
    # Perguntar a versão do dataset
    dataset_id = f"COP-DEM_GLO-30-DGED__{ask_dataset_version()}"
    
    # Perguntar se deseja substituir arquivos existentes
    replace_existing = ask_replace_existing()

    # Saídas intermediárias
    filled_dem = os.path.join(output_dir, "filled_dem.tif")
    flow_direction = os.path.join(output_dir, "flow_direction.tif")
    flow_accumulation = os.path.join(output_dir, "flow_accumulation.tif")
    streams = os.path.join(output_dir, "streams.tif")
    stream_vector = os.path.join(output_dir, "stream_vector.shp")
    strahler_order_raster = os.path.join(output_dir, "strahler_order.tif")
    streams_with_z = os.path.join(output_dir, "streams_with_z.shp")
    
    print("\033[1;32mProcessing DEM...\033[0m")
    
    # Passo 1: Preenchimento de Depressões
    wbt.fill_depressions(valid_dem, filled_dem)

    # Passo 2: Cálculo da Direção do Fluxo
    wbt.d8_pointer(filled_dem, flow_direction)

    # Passo 3: Cálculo da Acumulação do Fluxo
    wbt.d8_flow_accumulation(filled_dem, flow_accumulation, out_type='cells')

    # Passo 4: Extração das Linhas de Drenagem
    # Defina um limiar de acumulação para considerar como drenagem. Aqui estamos usando 1000 como exemplo.
    threshold = 1000
    wbt.extract_streams(flow_accumulation, streams, threshold)

    # Passo 5: Conversão das Drenagens para Vetor (Shapefile)
    wbt.raster_streams_to_vector(streams, flow_direction, stream_vector)

    # Passo 6: Classificação Strahler
    wbt.strahler_stream_order(flow_direction, streams, strahler_order_raster)

    # Passo 7: Atribuição das Coordenadas Z às Drenagens
    # Carregar o shapefile das drenagens
    gdf = gpd.read_file(stream_vector)

    # Abrir o DEM usando gdal
    dem_dataset = gdal.Open(valid_dem)
    dem_band = dem_dataset.GetRasterBand(1)

    # Adicionar a coluna Z ao GeoDataFrame
    gdf['elevation'] = add_elevation_to_gdf(gdf, dem_band, dem_dataset)

    # Salvar novamente o shapefile com as coordenadas Z adicionadas
    gdf.to_file(streams_with_z)

    print("Processamento completo.")

if __name__ == "__main__":
    main()
