<template>
    <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height:400px">
      <ol-view :center="center" :rotation="rotation" :zoom="zoom"
      :projection="projection" />
      <ol-tile-layer>
          <ol-source-osm />
      </ol-tile-layer>
    </ol-map>
  </template>

<script setup>
import { ref } from 'vue'
const center = ref([8.4, 49.0143])
const projection = ref('EPSG:4326')
const zoom = ref(14)
const rotation = ref(0)
</script>



<style scoped>
@import 'vue3-openlayers/dist/vue3-openlayers.css';
</style>