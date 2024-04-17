import csv
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsField, QgsRaster, QgsRasterCalculator, QgsExpression, QgsMapLayerRegistry

# Load CSV file containing rainfall data
csv_file_path = '/path/to/your/rainfall_data.csv'

# Define the field names for latitude, longitude, and rainfall
latitude_field = 'latitude'
longitude_field = 'longitude'
rainfall_field = 'rainfall'

# Define the output raster file path
output_raster_path = '/path/to/your/output_raster.tif'

# Create a memory layer to store the point features
point_layer = QgsVectorLayer("Point", "rainfall_points", "memory")
provider = point_layer.dataProvider()

# Add fields to the point layer
provider.addAttributes([QgsField(latitude_field,  QVariant.Double),
                        QgsField(longitude_field, QVariant.Double),
                        QgsField(rainfall_field,  QVariant.Double)])

# Load data from CSV file to memory layer
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        feature = QgsFeature()
        point = QgsPoint(float(row[longitude_field]), float(row[latitude_field]))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes([float(row[latitude_field]), float(row[longitude_field]), float(row[rainfall_field])])
        provider.addFeatures([feature])

# Add the memory layer to the map
QgsProject.instance().addMapLayer(point_layer)

# Set up the raster layer for rainfall analysis
xmin, ymin, xmax, ymax = point_layer.extent().toRectF().getCoords()
pixel_size = 0.01  # Adjust this according to your preference
raster_width = int((xmax - xmin) / pixel_size)
raster_height = int((ymax - ymin) / pixel_size)

# Generate raster layer from point layer
output_raster = QgsRasterLayer('Point?crs=EPSG:4326&field={}&field={}&field={}&index=2'.format(latitude_field, longitude_field, rainfall_field),
                               'rainfall_raster',
                               'memory',
                               raster_width,
                               raster_height,
                               QgsRectangle(xmin, ymin, xmax, ymax))

# Perform rainfall analysis using QgsRasterCalculator
exp = QgsExpression('"{0}"'.format(rainfall_field))
calc = QgsRasterCalculator(exp, output_raster_path, 'GTiff', output_raster.extent(), output_raster.width(), output_raster.height())
calc.processCalculation()

# Add the output raster to the map
output_raster = QgsRasterLayer(output_raster_path, 'Rainfall Analysis')
QgsProject.instance().addMapLayer(output_raster)

# Refresh the map canvas
iface.mapCanvas().refresh()
