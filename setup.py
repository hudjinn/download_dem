import os
import subprocess
import sys

# Função para instalar pacotes do sistema
def install_system_packages():
    try:
        if sys.platform.startswith('linux'):
            print("Updating package list and installing system dependencies...")
            subprocess.check_call(['sudo', 'apt-get', 'update'])
            subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'build-essential', 'python3-dev', 'gdal-bin', 'libgdal-dev'])
            print("System dependencies installed successfully.")
        elif sys.platform == 'win32':
            print("Please manually install GDAL from: https://gdal.org/download.html#download")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error installing system packages: {e}")
        sys.exit(1)

# Função para instalar pacotes Python
def install_python_packages():
    try:
        print("Installing Python packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Python packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python packages: {e}")
        sys.exit(1)

# Função para definir variáveis de ambiente no Linux
def set_environment_variables():
    if sys.platform.startswith('linux'):
        os.environ['CPLUS_INCLUDE_PATH'] = '/usr/include/gdal'
        os.environ['C_INCLUDE_PATH'] = '/usr/include/gdal'
        os.environ['GDAL_DATA'] = '/usr/share/gdal'
        os.environ['GDAL_DRIVER_PATH'] = '/usr/lib/gdalplugins'
        os.environ['PROJ_LIB'] = '/usr/share/proj'
        print("Environment variables set successfully.")
    elif sys.platform == 'win32':
        print("Please set the GDAL environment variables manually for Windows.")
        sys.exit(1)

# Função principal
def main():
    # Verificar se as dependências do sistema estão instaladas
    install_system_packages()

    # Definir variáveis de ambiente
    set_environment_variables()

    # Instalar pacotes Python
    install_python_packages()

    # Execute o script de download e processamento após a instalação
    print("Running download_dem.py...")
    subprocess.check_call([sys.executable, 'download_copernicus_dem.py'])

    print("Running process_dem.py...")
    subprocess.check_call([sys.executable, 'process_dem.py'])

if __name__ == "__main__":
    main()
