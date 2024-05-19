# Download DEM

Este repositório contém um script para download de Modelos Digitais de Elevação (DEM). Este projeto foi criado para facilitar o download de dados topográficos de alta resolução para uso em diversos aplicativos geoespaciais.

## Funcionalidades

- **Download Automático:** Baixa arquivos DEM de uma fonte específica.
- **Configuração Personalizável:** Permite aos usuários definir parâmetros como a área de interesse e a resolução desejada.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - requests
  - re
  - urllib3

## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/hudjinn/download_dem.git
    cd download_dem
    ```

2. Instale as dependências:
    ```sh
    pip3 install requests
    ```

## Uso

1. Configure os parâmetros no arquivo `bbox.json`:
    ```json
    {
      "area_of_interest": {
        "min_lat": -10.0,
        "max_lat": -5.0,
        "min_lon": -40.0,
        "max_lon": -35.0
      },
      "resolution": "30m" 
    }
    ```
    - `area_of_interest`: Define a área de interesse em formato de retângulo. Os valores devem ser fornecidos em graus
    - `resolution`: Define a resolução desejada para o DEM. Os valores possíveis são: `90m`, `30m` para Copernicus DEM

2. Execute o script de download dos modelos digitais de elevação COPERNICUS:
    ```sh
    sudo python3 download_copernicus_dem.py
    ```

## Estrutura do Projeto

```plaintext
download_dem/
├── README.md
├── config.json
└── download_copernicus_dem.py