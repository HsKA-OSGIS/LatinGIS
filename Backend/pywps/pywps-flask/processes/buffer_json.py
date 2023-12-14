from pywps import Process, LiteralInput, ComplexOutput, FORMATS
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import geopandas as gpd
import json
# Test
class BufferProcess(Process):
    def __init__(self):
        inputs = [
            LiteralInput('input_geojson', 'Input GeoJSON file', data_type='string'),
            LiteralInput('buffer_distance', 'Buffer distance', data_type='float'),
        ]
        outputs = [
            ComplexOutput('buffered_geojson', 'Buffered GeoJSON file', as_reference=True, supported_formats=[FORMATS.GEOJSON]),
        ]

        super(BufferProcess, self).__init__(
            self._handler,
            identifier='buffer_process',
            title='Buffer Process',
            abstract='A simple process to perform buffering on GeoJSON features.',
            version='1.0',
            inputs=inputs,
            outputs=outputs,
        )

    def _handler(self, request, response):
        input_geojson = request.inputs['input_geojson'][0].data
        buffer_distance = request.inputs['buffer_distance'][0].data

        # Read GeoJSON file
        gdf = gpd.read_file(input_geojson)

        # Perform buffer operation
        gdf['geometry'] = gdf['geometry'].buffer(buffer_distance)

        # Merge all geometries into a single geometry
        result_geometry = unary_union(gdf['geometry'])

        # Convert the result to GeoJSON
        result_geojson = json.dumps(mapping(result_geometry))

        # Save the result to a temporary GeoJSON file
        result_file = 'buffered_result.geojson'
        with open(result_file, 'w') as f:
            f.write(result_geojson)

        # Set the output reference
        response.outputs['buffered_geojson'].file = result_file

        return response