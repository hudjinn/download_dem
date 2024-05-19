import os
import requests
import re
import json
import urllib3

# Suprimir avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL
base_url = "https://prism-dem-open.copernicus.eu/pd-desk-open-access"

# Função para listar datasets disponíveis
def list_datasets():
    response = requests.get(f"{base_url}/publicDemURLs", headers={"accept": "json"}, verify=False)
    response.raise_for_status()
    return response.json()

# Função para listar URLs de DEM para um dataset específico
def list_dem_urls(dataset_id):
    response = requests.get(f"{base_url}/publicDemURLs/{dataset_id.replace('/', '__')}", headers={"accept": "json"}, verify=False)
    response.raise_for_status()
    return response.json()

# Função para baixar arquivos DEM
def download_file(url, output_dir, replace_existing):
    local_filename = os.path.join(output_dir, url.split('/')[-1])
    
    if not replace_existing and os.path.exists(local_filename):
        print(f"File already exists and will not be replaced: {local_filename}")
        return
    
    response = requests.get(url, stream=True, verify=False)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded: {local_filename}")

# Função para extrair coordenadas a partir do nome do arquivo
def extract_coordinates(filename):
    match = re.match(r"Copernicus_DSM_10_([NS]\d{2})_00_([EW]\d{3})_00\.tar", filename)
    if match:
        lat_str, lon_str = match.groups()
        
        lat = int(lat_str[1:]) * (-1 if lat_str[0] == 'S' else 1)
        lon = int(lon_str[1:]) * (-1 if lon_str[0] == 'W' else 1)
        
        return lat, lon
    return None, None

# Carregar parâmetros do arquivo bbox.json
with open('bbox.json') as f:
    params = json.load(f)
area_of_interest = params["area_of_interest"]
resolution = params["resolution"]

# Função para perguntar a versão do dataset
def ask_dataset_version(datasets):
    print("\033[1;34mSelect the dataset version:\033[0m")
    versions = {}
    for i, dataset in enumerate(datasets):
        dataset_name = dataset['datasetId'][:7]
        dataset_type = dataset['datasetId'][15:19]
        dataset_accuracy = dataset['datasetId'][12:14]
        dataset_version = dataset['datasetId'][20:]
        version_display = f"{dataset_name} | {dataset_type} | Spatial Resolution:{dataset_accuracy}m | Version: {dataset_version}"
        versions[str(i + 1)] = dataset['datasetId']
        print(f"[{i + 1}] - {version_display}")
    print(f"\033[1;90mHelp:\tDGED (Digital Elevation Data)\n\tDTED (Digital Terrain Elevation Data)\033[0m")
    choice = input("\033[1;34mEnter your choice: \033[0m").strip()
    dataset_url = versions.get(choice, None)

    return dataset_url  # Return None if invalid choice

# Função para perguntar se deseja substituir arquivos existentes
def ask_replace_existing():
    choice = input("\033[1;34mDo you want to redownload and replace existing files? (y/n): \033[0m").strip().lower()
    if choice == 'y':
        return True
    else:
        return False

# Função principal
def main():
    # Perguntar a versão do dataset
    print("\033[1;32mListing available datasets...\033[0m")
    datasets = list_datasets()
    dataset_id = ask_dataset_version(datasets=datasets)
    
    # Perguntar se deseja substituir arquivos existentes
    replace_existing = ask_replace_existing()
    
    # Criar diretório de download se não existir
    output_dir = "downloaded"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\033[1;32mListing DEM URLs for dataset {dataset_id}...\033[0m")
    dem_urls = list_dem_urls(dataset_id)
    print(f"\033[1;32mTotal DEM files: {len(dem_urls)}\033[0m")

    print("\033[1;32mFiltering URLs for the specified area of interest...\033[0m")
    filtered_urls = []
    for item in dem_urls:
        url = item["nativeDemUrl"]
        filename = url.split('/')[-1]
        print(filename)
        lat, lon = extract_coordinates(filename)
        if area_of_interest["min_lat"] <= lat <= area_of_interest["max_lat"] and area_of_interest["min_lon"] <= lon <= area_of_interest["max_lon"]:
            filtered_urls.append(url)
    print(f"\033[1;32mFiltered DEM files: {len(filtered_urls)}\033[0m")

    print("\033[1;32mDownloading DEM files...\033[0m")
    for url in filtered_urls:
        try:
            download_file(url, output_dir, replace_existing)
        except requests.HTTPError as e:
            print(f"\033[1;31mFailed to download {url}: {e}\033[0m")
    print("\033[1;32mDownload complete.\033[0m")

if __name__ == "__main__":
    main()
