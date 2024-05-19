import os
import tarfile
import rasterio
from rasterio.merge import merge
from shapely.geometry import shape, mapping
import geopandas as gpd
import fiona
from whitebox import WhiteboxTools

# Function to identify DEM source
def identify_dem_source(dem_dir):
    for root, dirs, files in os.walk(dem_dir):
        for file in files:
            if "Copernicus" in file:
                return "Copernicus"
    return None

# Function to extract TIFF files from Copernicus DEM
def extract_tiff_from_copernicus(dem_dir, output_dir):
    for root, dirs, files in os.walk(dem_dir):
        for file in files:
            if file.endswith(".tar"):
                tar_path = os.path.join(root, file)
                with tarfile.open(tar_path, "r") as tar:
                    for member in tar.getmembers():
                        if member.name.endswith(".tif") and "DEM" in member.name:
                            member.name = os.path.basename(member.name)
                            tar.extract(member, output_dir)
            else:
                continue

# Function to merge TIFF files
def merge_tiff_files(input_dir, output_filepath):
    tiff_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.tif')]
    print(tiff_files)
    exit()
    src_files_to_mosaic = [rasterio.open(fp) for fp in tiff_files]
    mosaic, out_trans = merge(src_files_to_mosaic)
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({"driver": "GTiff",
                     "height": mosaic.shape[1],
                     "width": mosaic.shape[2],
                     "transform": out_trans})
    with rasterio.open(output_filepath, "w", **out_meta) as dest:
        dest.write(mosaic)

# Function to process DEM
def process_dem(dem_filepath, output_dir):
    wbt = WhiteboxTools()
    wbt.set_working_dir(output_dir)

    # Convert DEM to a format compatible with WhiteboxTools
    dem_wbt = os.path.join(output_dir, "dem.tif")
    with rasterio.open(dem_filepath) as src:
        profile = src.profile
        profile.update(driver='GTiff')
        with rasterio.open(dem_wbt, 'w', **profile) as dst:
            dst.write(src.read(1), 1)

    # Fill depressions
    dem_filled = os.path.join(output_dir, "dem_filled.tif")
    wbt.fill_depressions(dem_wbt, dem_filled)

    # Flow accumulation
    flow_accumulation = os.path.join(output_dir, "flow_accumulation.tif")
    wbt.d8_flow_accumulation(dem_filled, flow_accumulation)

    # Flow direction
    flow_direction = os.path.join(output_dir, "flow_direction.tif")
    wbt.d8_pointer(dem_filled, flow_direction)

    # Stream extraction
    streams = os.path.join(output_dir, "streams.tif")
    wbt.extract_streams(flow_accumulation, streams, threshold=1000)

    # Stream to vector
    streams_shp = os.path.join(output_dir, "streams.shp")
    wbt.raster_streams_to_vector(streams, flow_direction, streams_shp)

    # Contours
    contours_shp = os.path.join(output_dir, "contours.shp")
    wbt.contour(dem_filled, contours_shp, interval=10)

    return streams_shp, contours_shp

# Function to clean up files
def clean_up_files(dem_dir, remove_downloaded):
    if remove_downloaded:
        for root, dirs, files in os.walk(dem_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))

# Main function
def main():
    # Directories
    downloaded_dir = "downloaded"
    output_dir = "output"
    
    # Create necessary directories
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Identify DEM source
    dem_source = identify_dem_source(downloaded_dir)
    print(f"DEM Source: {dem_source}")

    # Extract TIFF files based on DEM source
    if dem_source == "Copernicus":
        extract_tiff_from_copernicus(downloaded_dir, downloaded_dir)

    # Merge TIFF files
    merged_dem = os.path.join(output_dir, "merged_dem.tif")
    merge_tiff_files(downloaded_dir, merged_dem)
    print("DEM files merged successfully.")

    # Process DEM
    streams_shp, contours_shp = process_dem(merged_dem, output_dir)
    print(f"Streams and contours extracted: {streams_shp}, {contours_shp}")

    # Ask if user wants to remove downloaded files
    remove_downloaded = input("Do you want to remove the files from the downloaded folder? (y/n): ").strip().lower() == 'y'
    clean_up_files(downloaded_dir, remove_downloaded)
    if remove_downloaded:
        print("Downloaded files removed.")
    else:
        print("Downloaded files kept.")

if __name__ == "__main__":
    main()
