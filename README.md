# Download DEM

Este repositório contém scripts para download e processamento de Modelos Digitais de Elevação (DEM). Este projeto foi criado para facilitar o download de dados topográficos de alta resolução para uso em diversos aplicativos geoespaciais.

## Funcionalidades

- **Download Automático:** Baixa arquivos DEM de uma fonte específica.
- **Configuração Personalizável:** Permite aos usuários definir parâmetros como a área de interesse e a resolução desejada.
- **Processamento de DEM:** Descompacta, mescla e processa arquivos DEM, extraindo drenagens e curvas de nível.

## Requisitos

- Python 3.x

## Instalação

### Linux

1. Clone o repositório:
    ```sh
    git clone https://github.com/hudjinn/download_dem.git
    cd download_dem
    ```

2. Execute o script de instalação:
    ```sh
    sudo python setup.py
    ```

### Windows

Para usuários do Windows, siga os passos manuais para instalar o GDAL:

#### 1. Clonar o Repositório
Primeiro, você precisa clonar o repositório onde os scripts estão armazenados:

1. Abra o Prompt de Comando ou o PowerShell.
2. Digite o seguinte comando para clonar o repositório:
    ```sh
    git clone https://github.com/hudjinn/download_dem.git
    cd download_dem
    ```

#### 2. Baixar e Instalar o GDAL
Em seguida, você deve baixar e instalar o GDAL:

1. Vá para a página de [download do GDAL](https://gdal.org/download.html#download).
2. Baixe a versão adequada para o seu sistema operacional (provavelmente Windows 64-bit).
3. Extraia os arquivos para uma pasta de fácil acesso, por exemplo, `C:\gdal`.

#### 3. Configurar as Variáveis de Ambiente
Configurar as variáveis de ambiente permite que seu sistema encontre as bibliotecas e os dados necessários para o GDAL funcionar corretamente. Siga os passos abaixo:

1. **Abrir o Prompt de Comando como Administrador:**
    - Clique no menu Iniciar.
    - Digite `cmd`.
    - Clique com o botão direito em "Prompt de Comando" e selecione "Executar como administrador".

2. **Adicionar o Caminho do Binário do GDAL ao PATH:**
    - No Prompt de Comando, digite o seguinte comando e pressione Enter:
        ```sh
        setx PATH "%PATH%;C:\gdal\bin"
        ```

3. **Definir a Variável de Ambiente GDAL_DATA:**
    - Isso aponta para a localização dos dados do GDAL.
    - Digite o seguinte comando e pressione Enter:
        ```sh
        setx GDAL_DATA "C:\gdal\gdal-data"
        ```

4. **Definir a Variável de Ambiente GDAL_DRIVER_PATH:**
    - Isso aponta para a localização dos plugins do GDAL.
    - Digite o seguinte comando e pressione Enter:
        ```sh
        setx GDAL_DRIVER_PATH "C:\gdal\gdalplugins"
        ```

5. **Definir a Variável de Ambiente PROJ_LIB:**
    - Isso aponta para a localização dos arquivos de projeção.
    - Digite o seguinte comando e pressione Enter:
        ```sh
        setx PROJ_LIB "C:\gdal\projlib"
        ```

Esses comandos configuram o ambiente necessário para o GDAL funcionar corretamente no seu sistema.

#### 4. Instalar as Dependências Python
Depois de configurar o GDAL, você precisa instalar as bibliotecas Python necessárias:

1. **Certifique-se de que o Python e o pip estão instalados:**
    - Para verificar se o Python está instalado, abra o Prompt de Comando e digite:
        ```sh
        python --version
        ```
    - Para verificar se o pip está instalado, digite:
        ```sh
        pip --version
        ```

2. **Instalar as Dependências:**
    - No diretório `download_dem` (onde você clonou o repositório), digite:
        ```sh
        pip install -r requirements.txt
        ```

#### 5. Executar os Scripts
Agora que todas as dependências estão instaladas e o GDAL está configurado, você pode executar os scripts:

### Script de Download

1. **Modificar a Área de Interesse (BBox):**
    - Antes de executar o script de download, você pode configurar os parâmetros de área de interesse (`bbox`) no arquivo `bbox.json`. Abra o arquivo `bbox.json` em um editor de texto e ajuste os valores conforme a área que deseja processar. Exemplo:
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

2. **Executar o Script de Download:**
    - Execute o script de download para obter os arquivos DEM:
        ```sh
        python download_dem.py
        ```

### Script de Processamento

1. **Executar o Script de Processamento:**
    - Execute o script de processamento para extrair drenagens e curvas de nível:
        ```sh
        python process_dem.py
        ```

    Este script realizará os seguintes passos:
    - Descompactará os arquivos na pasta `downloaded`.
    - Ignorará arquivos que não sejam DEM.
    - Mesclará os arquivos DEM em um único arquivo.
    - Armazenará o resultado na pasta `input`.
    - Perguntará se o usuário deseja remover os arquivos da pasta `downloaded`.
    - Extrairá drenagens e curvas de nível.

## Uso

### Download de DEM

1. Edite os parâmetros no arquivo `bbox.json` caso deseje definir outra área de interesse para efetuar os downloads do DEM, por padrão está o Bounding Box para o Estado do Ceará, ou seja, vai efetuar o download dos tif que estão dentro do quadrado definido pelas 4 coordenadas:
    ```json
    {
        "area_of_interest": {
          "min_lat": -8.0,
          "max_lat": -2.0,
          "min_lon": -42.0,
          "max_lon": -38.0
        },
        "resolution": "30m"
      }
    ```

2. Execute o script de download:
    ```sh
    python download_copernicus_dem.py
    ```

### Processamento de DEM

1. Execute o script de processamento:
    ```sh
    python process_dem.py
    ```

    Este script realizará os seguintes passos:
    - Descompactará os arquivos na pasta `downloaded`.
    - Ignorará arquivos que não sejam DEM.
    - Mesclará os arquivos DEM em um único arquivo.
    - Armazenará o resultado na pasta `input`.
    - Perguntará se o usuário deseja remover os arquivos da pasta `downloaded`.
    - Extraíra drenagens e curvas de nível.

## Estrutura do Projeto

```plaintext
download_dem/
├── README.md
├── requirements.txt
├── bbox.json
├── download_dem.py
├── process_dem.py
└── input/
