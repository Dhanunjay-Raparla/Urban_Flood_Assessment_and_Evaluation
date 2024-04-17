import numpy as np
from osgeo import gdal

def save_asc(filename, data, xllcorner, yllcorner, cellsize, nodata_value):
    """
    Save data as .tiff file.
    """
    driver = gdal.GetDriverByName('AAIGrid')
    dataset = driver.Create(filename, data.shape[1], data.shape[0], 1, gdal.GDT_Float32)
    dataset.SetGeoTransform((xllcorner, cellsize, 0, yllcorner, 0, -cellsize))
    band = dataset.GetRasterBand(1)
    band.SetNoDataValue(nodata_value)
    band.WriteArray(data)
    dataset.FlushCache()


# Define parameters for .asc file
xllcorner = 0  # X-coordinate of the lower-left corner
yllcorner = 0  # Y-coordinate of the lower-left corner
cellsize = 1  # Size of each cell in the raster
nodata_value = -9999  # Nodata value for the raster

# Save the accumulation as .asc file
save_asc(output_file, accumulation, xllcorner, yllcorner, cellsize, nodata_value)


def calculate_flow_direction(aspect):
    """
    Calculate water flow direction based on slope aspect.
    """
    # Define flow direction based on slope aspect
    flow_direction = np.zeros(aspect.shape, dtype=int)
    flow_direction[(aspect > 337.5) | (aspect <= 22.5)] = 1  # East
    flow_direction[(aspect > 22.5) & (aspect <= 67.5)] = 2   # Northeast
    flow_direction[(aspect > 67.5) & (aspect <= 112.5)] = 3  # North
    flow_direction[(aspect > 112.5) & (aspect <= 157.5)] = 4  # Northwest
    flow_direction[(aspect > 157.5) & (aspect <= 202.5)] = 5  # West
    flow_direction[(aspect > 202.5) & (aspect <= 247.5)] = 6  # Southwest
    flow_direction[(aspect > 247.5) & (aspect <= 292.5)] = 7  # South
    flow_direction[(aspect > 292.5) & (aspect <= 337.5)] = 8  # Southeast
    return flow_direction

def calculate_accumulation(gradient, flow_direction):
    """
    Calculate water accumulation based on flow direction and slope gradient.
    """
    accumulation = np.zeros_like(gradient, dtype=float)
    rows, cols = gradient.shape
    for i in range(1, rows-1):
        for j in range(1, cols-1):
            # Calculate accumulation for each pixel based on flow direction
            if flow_direction[i, j] == 1:  # East
                accumulation[i, j+1] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 2:  # Northeast
                accumulation[i-1, j+1] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 3:  # North
                accumulation[i-1, j] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 4:  # Northwest
                accumulation[i-1, j-1] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 5:  # West
                accumulation[i, j-1] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 6:  # Southwest
                accumulation[i+1, j-1] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 7:  # South
                accumulation[i+1, j] += accumulation[i, j] + gradient[i, j]
            elif flow_direction[i, j] == 8:  # Southeast
                accumulation[i+1, j+1] += accumulation[i, j] + gradient[i, j]
    return accumulation

# File paths for slope gradient and aspect
slope_gradient_file = "slope_gradient.asc"
slope_aspect_file = "slope_aspect.asc"

# Read slope gradient and aspect data
slope_gradient = read_asc(slope_gradient_file)
slope_aspect = read_asc(slope_aspect_file)

# Calculate flow direction based on slope aspect
flow_direction = calculate_flow_direction(slope_aspect)

# Calculate water accumulation
accumulation = calculate_accumulation(slope_gradient, flow_direction)

# Output or visualize the results as needed
# For example, you can save the accumulation as a new .asc file
# Write code to save the accumulation array as an .asc file
def save_geotiff(filename, data, xllcorner, yllcorner, cellsize, nodata_value):
    """
    Save data as GeoTIFF file.
    """
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(filename, data.shape[1], data.shape[0], 1, gdal.GDT_Float32)
    dataset.SetGeoTransform((xllcorner, cellsize, 0, yllcorner, 0, -cellsize))
    band = dataset.GetRasterBand(1)
    band.SetNoDataValue(nodata_value)
    band.WriteArray(data)
    dataset.FlushCache()

# File paths for saving the accumulation
output_geotiff = "water_accumulation.tif"

# Save the accumulation as GeoTIFF file
save_geotiff(output_geotiff, accumulation, xllcorner, yllcorner, cellsize, nodata_value)

# Define parameters for .asc file
xllcorner = 0  # X-coordinate of the lower-left corner
yllcorner = 0  # Y-coordinate of the lower-left corner
cellsize = 1  # Size of each cell in the raster
nodata_value = -9999  # Nodata value for the raster

# Save the accumulation as .asc file
save_asc(output_file, accumulation, xllcorner, yllcorner, cellsize, nodata_value)

