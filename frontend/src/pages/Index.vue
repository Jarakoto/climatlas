<template>
  <q-page class="row items-center justify-evenly">
    <search-bar />
    <div id="map" />
  </q-page>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue'
import { Map } from 'maplibre-gl'
import SearchBar from 'src/components/HomePage/SearchBar.vue'

let map: Map

export default defineComponent(
  {
    components: { SearchBar },
    name: 'PageIndex',
    setup () {
      onMounted(() => {
        map = new Map({
          container: 'map',
          style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL', // stylesheet location
          center: [2.213749, 46.227638], // starting position [lng, lat]
          zoom: 5.5 // starting zoom
        })
      })
    }
  }
)

export { map }
</script>

<style lang="scss">
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
