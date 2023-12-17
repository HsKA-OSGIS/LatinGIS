<template>
  <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 480px" ref="map">
    <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />


    <ol-tile-layer ref="osmLayer">
      <ol-source-osm />
    </ol-tile-layer>
    <!--Points layer from api geojson-->
    <ol-webgl-points-layer  v-for="(layer, index) in layers" :key="index" :styles="layer.styles" :title="layer.name">
      <ol-source-webglpoints :format="geoJson" :url="layer.url" />
    </ol-webgl-points-layer>

    <!--Point Marker on the map-->
    <ol-context-menu-control @contextmenu="addMarker" />
    <!--Layer switcher control-->
    <ol-layerswitcher-control />

    <!--geolocation for user of the app-->
    <ol-geolocation :projection="projection" @change:position="geoLocChange">
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
  </ol-map>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";
import hereIcon from "/here.png";
import type { View } from "ol";
import type { ObjectEvent } from "ol/Object";
import { inject } from 'vue';
import { GeoJSON } from 'ol/format';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';


const format = inject("ol-format");
const geoJson = new GeoJSON();

const center = ref([40, 40]);
const projection = ref("EPSG:3857");
const zoom = ref(14);
const rotation = ref(0);
const view = ref<View | null>(null);
const map = ref(null);
const position = ref<number[]>([]);
const layerList = ref([]);
const osmLayer = ref(null);
const markers = ref(null);

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
    "circle-opacity": [ "interpolate",
        ["linear"],
        ["get", "population"],
        40000,
        0.6,
        2000000,
        0.92,
      ]
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
      ]
    }
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
      ]
    }
  },
  {
    name: 'Sport Facilities',
    url:'https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Sportanlagen/MapServer/4/query?where=GRUPPENNAME_DE+%3D+%27Sporthallen%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson',
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
      ]
    }
  }
]);
onMounted(() => {
  layerList.value.push(osmLayer.value.tileLayer)
});

const geoLocChange = (event: ObjectEvent) => {
  console.log("AAAAA", event);
  position.value = event.target.getPosition();
  view.value?.setCenter(event.target?.getPosition());
};

const addMarker = (event) => {
  const feature = new Feature({
    geometry: new Point(event.coordinate),
  });
  markers.value.source.addFeature(feature);
};


</script>