import requests
import re
import json
import urllib3

# Suprimir avisos de InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL
base_url = "https://prism-dem-open.copernicus.eu/pd-desk-open-access"

def list_datasets():
    response = requests.get(f"{base_url}/publicDemURLs", headers={"accept": "json"}, verify=False)
    response.raise_for_status()
    return response.json()

def list_dem_urls(dataset_id):
    response = requests.get(f"{base_url}/publicDemURLs/{dataset_id.replace('/', '__')}", headers={"accept": "json"}, verify=False)
    response.raise_for_status()
    return response.json()

def download_file(url):
    local_filename = url.split('/')[-1]
    response = requests.get(url, stream=True, verify=False)
    response.raise_for_status()
    with open(local_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded: {local_filename}")

# Função para extrair a latitude e longitude a partir do nome do arquivo
def extract_coordinates(filename):
    match = re.match(r"Copernicus_DSM_10_([NS]\d{2})_00_([EW]\d{3})_00\.tar", filename)
    if match:
        lat_str, lon_str = match.groups()
        
        lat = int(lat_str[1:]) * (-1 if lat_str[0] == 'S' else 1)
        lon = int(lon_str[1:]) * (-1 if lon_str[0] == 'W' else 1)
        
        return lat, lon
    return None, None

def main():
    # Carregar parâmetros da área de interesse a partir do arquivo bbox.json
    with open('bbox.json', 'r') as f:
        bbox = json.load(f)

    print("Listing available datasets...")
    datasets = list_datasets()
    print(f"Available datasets: {datasets}")

    # Seleciona o dataset desejado
    dataset_id = "COP-DEM_GLO-30-DGED__2023_1"
    print(f"Listing DEM URLs for dataset {dataset_id}...")
    dem_urls = list_dem_urls(dataset_id)
    print(f"Total DEM files: {len(dem_urls)}")

    print("Filtering URLs for the area of interest...")
    filtered_urls = []
    for item in dem_urls:
        url = item["nativeDemUrl"]
        filename = url.split('/')[-1]
        lat, lon = extract_coordinates(filename)
        if bbox["area_of_interest"]["min_lat"] <= lat <= bbox["area_of_interest"]["max_lat"] and bbox["area_of_interest"]["min_lon"] <= lon <= bbox["area_of_interest"]["max_lon"]:
            filtered_urls.append(url)
    print(f"Filtered DEM files: {len(filtered_urls)}")

    print("Downloading DEM files...")
    for url in filtered_urls:
        try:
            download_file(url)
        except requests.HTTPError as e:
            print(f"Failed to download {url}: {e}")
    print("Download complete.")

if __name__ == "__main__":
    main()
