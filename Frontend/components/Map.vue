<template>
  <div class="relative">
    <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 480px" ref="map">
      <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />
      <ol-tile-layer ref="osmLayer">
        <ol-source-osm />

      </ol-tile-layer>
      <!--Points layer from api geojson-->
      <ol-webgl-points-layer v-for="(layer, index) in layers" :key="index" :styles="layer.styles" v-if="selectedLayer1">
        <ol-source-webglpoints :format="geoJson" :url="layer.url" />
      </ol-webgl-points-layer>

      <!--Point Marker on the map-->
      <ol-context-menu-control @contextmenu="contextMenuItems" />
      <ol-vector-layer>
        <ol-source-vector ref="markers"> </ol-source-vector>
        <ol-style>
          <ol-style-icon :src="hereIcon" :scale="0.1"></ol-style-icon>
        </ol-style>
      </ol-vector-layer>
      <!--Layer switcher control-->


      <!--geolocation for user of the app-->
      <ol-geolocation :projection="projection" @change:position="geoLocChange" v-if="checked">
        <template>
          <ol-vector-layer :zIndex="2" :title="currentLocation.title">
            <ol-source-vector>
              <ol-feature ref="positionFeature">
                <ol-geom-point :coordinates="position"></ol-geom-point>
                <ol-style>
                  <ol-style-icon :src="hereIcon" :scale="0.03"></ol-style-icon>
                </ol-style>
              </ol-feature>
            </ol-source-vector>
          </ol-vector-layer>
        </template>
      </ol-geolocation>
      <ol-fullscreen-control />
      <ol-scaleline-control />
      <ol-control-bar>
      <ol-toggle-control
        html="🟢"
        className="edit"
        title="Circle"
        :onToggle="(active: boolean) => changeDrawType(active, 'Circle')"
      />
      <ol-toggle-control
      html="🔺"
      className="edit"
      title="Polygon"
      :onToggle="(active: boolean) => changeDrawType(active, 'Polygon')"
    />
    </ol-control-bar>

    <ol-interaction-draw
      :type="drawType"
      @drawend="drawend"
      @drawstart="drawstart"
    >
    </ol-interaction-draw>

    </ol-map>
  </div>

  <div class="absolute bottom-10 right-0">
    <!--Toolbar component-->
    <div class=" bg-white max-w-md mx-auto bg-white rounded-xl overflow-hidden p-6 shadow-md">
      <h2 class="text-2xl font-semibold mb-4">Map Controls</h2>
      <div class="flex flex-wrap space-x-2">
        <!-- Map Layer Options (Example options, replace with your actual options) -->
        <!-- Map Layers Section -->
        <div class="mb-4">
          <h3 class="text-lg font-semibold mb-2">Map Layers</h3>
          <label class="flex items-center space-x-1">
            <input type="checkbox" class="form-checkbox text-indigo-500"  v-model="selectedLayer1">
            <span>Feature Collection Layers</span>
          </label>
          <label class="flex items-center space-x-1">
            <input type="checkbox" class="form-checkbox"  v-model="checked">
            <span>Location</span>

          </label>
        </div>
      </div>

      <!-- WPS Parameters Section -->
      <div class="mb-4">
        <h3 class="text-lg font-semibold mb-2">WPS Parameters</h3>
        <div class="flex flex-wrap space-x-2">
          <!-- WPS Parameter Options (Example options, replace with your actual options) -->
          <label class="flex items-center space-x-1">
            <input type="radio" class="walk" name="go" value="short">
            <span>Walking</span>
          </label>
          <label class="flex items-center space-x-1">
            <input type="radio" class="Bike" name="go" value="short">
            <span>Bike</span>
          </label>
          <!-- Add more parameters as needed -->
        </div>
      </div>

      <!-- Travel Distance Section -->
      <div>
        <h3 class="text-lg font-semibold mb-2">Travel Distance</h3>
        <div class="flex items-center space-x-2">
          <!-- Travel Distance Options (Example options, replace with your actual options) -->
          <label class="flex items-center space-x-1">
            <input type="radio" class="form-radio" name="distance" value="short">
            <span>5 min</span>
          </label>
          <label class="flex items-center space-x-1">
            <input type="radio" class="form-radio" name="distance" value="medium">
            <span>10 min</span>
          </label>
          <label class="flex items-center space-x-1">
            <input type="radio" class="form-radio" name="distance" value="long">
            <span>15 min</span>
          </label>
        </div>
      </div>
      <!-- Calculate Button (Centered) -->
      <div class="flex justify-center mt-4">
        <button @click="performWpsRequest" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Calculate
        </button>
      </div>
    </div>
    
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import hereIcon from "/here.png";
import type { View } from "ol";
import type { ObjectEvent } from "ol/Object";
import { inject } from 'vue';
import 'ol/ol.css';
import { GeoJSON } from 'ol/format';
import type { DrawEvent } from 'ol/interaction/Draw';
import type { Feature } from 'ol';
import type Geometry from 'ol/geom/Geometry';
import { Vector as VectorSource } from "ol/source";
import VectorLayer from "ol/layer/Vector";

const markers = ref<VectorLayer<VectorSource<Feature<Geometry>>>>(new VectorLayer({
  source: new VectorSource(),
}));


const format = inject("ol-format");
const geoJson = new GeoJSON();

const center = ref([8, 49]);
const projection = ref("EPSG:3857");
const zoom = ref(14);
const rotation = ref(0);
const view = ref<View | null>(null);
const map = ref(null);
const position = ref<number[]>([]);
const layerList = ref([]);
const osmLayer = ref(null);
const contextMenuItems = ref([]);
const checked = ref(false);
const selectedLayer1 = ref(false);
const selectedLayer2 = ref(false);
const selectedLayer3 = ref(false);



const drawEnable = ref(false);
const drawType = ref("Circle");
const drawnFeatures = ref<Feature<Geometry>[]>([]);
const drawnPolygon = ref<string | null>(null);
  const performWpsRequest = async () => {
  try {
    if (drawnPolygon.value) {
      const wpsUrl = `http://localhost/cgi-bin/zoo_loader.cgi?service=WPS&version=1.0.0&request=Execute&identifier=Buffer&DataInputs=InputPolygon=${drawnPolygon.value}&BufferDistance=20.0`;
      const response = await fetch(wpsUrl);
      const result = await response.json();
      // Procesar el resultado según sea necesario
      console.log(result);
    } else {
      console.error('No hay polígono dibujado para enviar a la petición WPS.');
    }
  } catch (error) {
    console.error('Error al realizar la petición WPS:', error);
  }
};


const drawend = (event: DrawEvent) => {
  const feature = event.feature;
  if (feature) {
    const geometry = feature.getGeometry();
    if (geometry) {
      const geoJsonFormat = new GeoJSON();
      const geoJson = geoJsonFormat.writeGeometry(geometry, {
        dataProjection: 'EPSG:4326',
        featureProjection: 'EPSG:3857',
      });
      drawnPolygon.value = encodeURIComponent(geoJson);
    } else {
      console.error('La geometría del polígono dibujado es undefined.');
    }
  } else {
    console.error('El feature del polígono dibujado es undefined.');
  }

  drawnFeatures.value.forEach((prevFeature) => {
    markers.value?.getSource()?.removeFeature(prevFeature);
  });

  // Add the new circle to the drawnFeatures array
  drawnFeatures.value = [feature as Feature<Geometry>];
  console.log(event);
};



const changeDrawType = (active: boolean, draw: string) => {
  drawEnable.value = active;
  drawType.value = draw;
};

const drawstart = (event: DrawEvent) => {
  drawnFeatures.value = [];
  console.log(event);
};














const currentLocation = {
  "title": "My Location"
};

interface Layer {
  name: string;
  url: string;
  styles: {
    "circle-radius": number;
    "circle-fill-color": string;
    "circle-stroke-width": number;
    "circle-stroke-color": string;
    "circle-opacity": ["interpolate",
      ["linear"],
      ["get", "population"],
      40000,
      0.6,
      2000000,
      0.92,
    ];
  };

 
}

const layers = ref<Layer[]>([
  {
    name: 'Hotels',
    url: 'https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Tourismus/MapServer/1/query?where=GRUPPENNAME_DE+%3D+%27Hotels/Unterk%C3%BCnfte%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson',
    styles: {
      "circle-radius": 6,
      "circle-fill-color": "yellow",
      "circle-stroke-width": 2,
      "circle-stroke-color": "darkblue",
      "circle-opacity": [
        "interpolate",
        ["linear"],
        ["get", "population"],
        40000,
        0.6,
        2000000,
        0.92,
      ],
    },
  
  },
  {
    name: 'Schools',
    url: 'https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Bestattungen/MapServer/0/query?where=GRUPPENNAME_DE+%3D+%27Bestattungsinstitute%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson',
    styles: {
      "circle-radius": 6,
      "circle-fill-color": "blue",
      "circle-stroke-width": 2,
      "circle-stroke-color": "darkblue",
      "circle-opacity": [
        "interpolate",
        ["linear"],
        ["get", "population"],
        40000,
        0.6,
        2000000,
        0.92,
      ],
    },
    
  },
  {
    name: 'Sport Facilities',
    url: 'https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Sportanlagen/MapServer/4/query?where=GRUPPENNAME_DE+%3D+%27Sporthallen%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson',
    styles: {
      "circle-radius": 6,
      "circle-fill-color": "orange",
      "circle-stroke-width": 2,
      "circle-stroke-color": "darkblue",
      "circle-opacity": [
        "interpolate",
        ["linear"],
        ["get", "population"],
        40000,
        0.6,
        2000000,
        0.92,
      ],
    },
    
  },
]);

const geoLocChange = (event: ObjectEvent) => {
  // Handle the geolocation change event
  console.log("Geolocation changed:", event);
  position.value = event.target.getPosition();
  view.value?.setCenter(event.target?.getPosition());

};









</script>

