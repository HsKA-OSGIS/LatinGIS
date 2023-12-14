<template>
  <ol-map
    ref="map"
    :loadTilesWhileAnimating="true"
    :loadTilesWhileInteracting="true"
    style="height: 480px"
  >
    <ol-view
      ref="view"
      :center="center"
      :rotation="rotation"
      :zoom="zoom"
      :projection="projection"
    />

    <ol-layerswitcher-control  />

  
    <ol-tile-layer ref="osmLayer" title="OSM">
      <ol-source-osm />
    </ol-tile-layer>


    <ol-control-bar>
      <ol-toggle-control
        html="🔘"
        className="edit"
        title="Point"
        :onToggle="(active) => changeDrawType(active, 'Point')"
      />
    
      <ol-printdialog-control />
    </ol-control-bar>

    
    <ol-fullscreen-control />
    <ol-overviewmap-control>
      <ol-tile-layer>
        <ol-source-osm />
      </ol-tile-layer>
    </ol-overviewmap-control>

    <ol-scaleline-control />
    
    <ol-zoom-control />
    

    <ol-context-menu-control :items="contextMenuItems" />

    <ol-interaction-clusterselect @select="featureSelected" :pointRadius="20">
      <ol-style>
        <ol-style-stroke color="green" :width="5"></ol-style-stroke>
        <ol-style-fill color="rgba(255,255,255,0.5)"></ol-style-fill>
        <ol-style-icon :src="markerIcon" :scale="0.1"></ol-style-icon>
      </ol-style>
    </ol-interaction-clusterselect>

   

    <ol-animated-clusterlayer>
      <ol-source-vector ref="vectorsource">
        <ol-feature v-for="index in 500" :key="index">
          <ol-geom-point
            title="Hotels"
            :coordinates="[
              getRandomInRange(24, 45, 3),
              getRandomInRange(35, 41, 3),
            ]"
          ></ol-geom-point>
        </ol-feature>
      </ol-source-vector>

      
    </ol-animated-clusterlayer>

   

   

    <ol-webgl-points-layer :styles="webglPointsStyle">
      <ol-source-webglpoints
        :format="geoJson"
        url="https://geoportal.karlsruhe.de/server/rest/services/Stadtplan/Stadtplan_POIs_Tourismus/MapServer/1/query?where=GRUPPENNAME_DE+%3D+%27Hotels/Unterk%C3%BCnfte%27&outFields=NAME%2CGRUPPENNAME_DE%2CUPDATED&returnGeometry=true&f=geojson"
      />
     
    </ol-webgl-points-layer>

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
  </ol-map>
</template>

<script setup>
import { ref, inject, onMounted } from "vue";
import markerIcon from "/here.png";

const center = ref([40, 40]);
const projection = ref("EPSG:3857");
const zoom = ref(14);
const position = ref([]);
const rotation = ref(0);
const format = inject("ol-format");
const geoJson = new format.GeoJSON();
const osmLayer = ref(null);
const layerList = ref([]);
const selectConditions = inject("ol-selectconditions");
const selectedCityName = ref("");
const selectedCityPosition = ref([]);
const extent = inject("ol-extent");
const Feature = inject("ol-feature");
const Geom = inject("ol-geom");
const contextMenuItems = ref([]);
const vectorsource = ref(null);
const view = ref(null);
const drawEnable = ref(false);
const drawType = ref("Point");
const currentLocation ={
"title":"My Location"
};

const geoLocChange = (event: ObjectEvent) => {
  console.log("AAAAA", event);
  position.value = event.target.getPosition();
  view.value?.setCenter(event.target?.getPosition());
};

const changeDrawType = (active, draw) => {
  drawEnable.value = active;
  drawType.value = draw;
};

contextMenuItems.value = [
 
  {
    text: "Add a Point",
    classname: "some-style-class", // you can add this icon with a CSS class
    // instead of `icon` property (see next line)
    icon: markerIcon, // this can be relative or absolute
    callback: (val) => {
      console.log(val);
      const feature = new Feature({
        geometry: new Geom.Point(val.coordinate),
      });
      vectorsource.value.source.addFeature(feature);
    },
  },
  "-", // this is a separator
];

const featureSelected = (event) => {
  if (event.selected.length == 1) {
    selectedCityPosition.value = extent.getCenter(
      event.selected[0].getGeometry().extent_,
    );
    selectedCityName.value = event.selected[0].values_.name;
  } else {
    selectedCityName.value = "";
  }
};

const overrideStyleFunction = (feature, style) => {
  const clusteredFeatures = feature.get("features");
  const size = clusteredFeatures.length;

  const color = size > 20 ? "192,0,0" : size > 8 ? "255,148,0" : "0,18,0";
  const radius = Math.max(8, Math.min(size, 20));
  const dash = (2 * Math.PI * radius) / 6;
  const calculatedDash = [0, dash, dash, dash, dash, dash, dash];

  style.getImage().getStroke().setLineDash(dash);
  style
    .getImage()
    .getStroke()
    .setColor("rgba(" + color + ",0.5)");
  style.getImage().getStroke().setLineDash(calculatedDash);
  style
    .getImage()
    .getFill()
    .setColor("rgba(" + color + ",1)");

  style.getImage().setRadius(radius);

  style.getText().setText(size.toString());
};

const selectInteactionFilter = (feature) => {
  return feature.values_.name != undefined;
};

const getRandomInRange = (from, to, fixed) => {
  return (Math.random() * (to - from) + from).toFixed(fixed) * 1;
};



const drawend = (event) => {
  console.log(event);
};

const modifystart = (event) => {
  console.log(event);
};

const modifyend = (event) => {
  console.log(event);
};






onMounted(() => {
  layerList.value.push(jawgLayer.value.tileLayer);
  layerList.value.push(osmLayer.value.tileLayer);
  console.log(layerList.value);
});

const path = ref([
  [25.6064453125, 44.73302734375001],
  [27.759765625, 44.75500000000001],
  [28.287109375, 43.32677734375001],
  [30.55029296875, 46.40294921875001],
  [31.69287109375, 43.04113281250001],
]);




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
</script>

<style scoped>
.overlay-content {
  background: #c84031;
  color: white;
  box-shadow: 0 5px 10px rgb(2 2 2 / 20%);
  padding: 10px 20px;
  font-size: 16px;
}
</style>