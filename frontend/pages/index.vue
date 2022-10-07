<template>
  <v-app>
    <v-main>
      <div id="search-location-bar-container" :style="{ width: '400px' }" class="pa-2">
        <div>
          <SearchBar />
        </div>
      </div>
      <div id="map"></div>
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
import { Map } from "maplibre-gl";
import SearchBar from "~/components/HomePage/SearchBar.vue";

let map: Map;

onMounted(() => {
  map = new Map({
    container: "map",
    style:
      "https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL", // stylesheet location
    center: [2.213749, 46.227638], // starting position [lng, lat]
    zoom: 5.5, // starting zoom
  });
});
</script>

<style lang="scss">
#search-location-bar-container {
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
}

#map {
  width: 100vw;
  height: 100vh;
  position: fixed;
  position: fixed;
  top: 0;
  .maplibregl-ctrl-attrib {
    display: none;
  }
}
</style>
