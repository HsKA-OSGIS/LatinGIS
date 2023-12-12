<template>
  <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 480px" ref="map">
    <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />

    <!--Load of the openstreet maps layer-->
    <ol-tile-layer>
      <ol-source-osm />
    </ol-tile-layer>


    <!--Points layer from api geojson-->
    <ol-webgl-points-layer :styles="webglPointsStyle">
      <ol-source-webglpoints :format="geoJson"
        url="https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Sportanlagen/MapServer/4/query?where=GRUPPENNAME_DE+%3D+%27Sporthallen%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson" />
    </ol-webgl-points-layer>
    <!--geolocation for user of the app-->

    <ol-geolocation :projection="projection" @change:position="geoLocChange">
      <template>
        <ol-vector-layer :zIndex="2">
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

<script setup lang="ts">
import hereIcon from "/here.png";
import { ref } from "vue";
import type { View } from "ol";
import type { ObjectEvent } from "ol/Object";
const format = inject("ol-format");
const geoJson = new format.GeoJSON();

const center = ref([40, 40]);
const projection = ref("EPSG:3857");
const zoom = ref(14);
const rotation = ref(0);
const view = ref<View>();
const map = ref(null);
const position = ref([]);

const webglPointsStyle = {
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
};

const geoLocChange = (event: ObjectEvent) => {
  console.log("AAAAA", event);
  position.value = event.target.getPosition();
  view.value?.setCenter(event.target?.getPosition());
};
</script>