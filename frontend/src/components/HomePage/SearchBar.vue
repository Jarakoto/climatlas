<template>
  <div id="home-search-bar" class="q-ma-sm q-py-xs shadow-1">
    <q-input id="home-search-bar-input" v-model="searchInputValue"
      type="search"
      dense use-input borderless style="width: 400px" class="q-px-md" label="Recherchez un lieu ou un nom de rue"
      v-on:keyup.enter="focusFirstLocation()"
      ref="searchInput"
      :options="locations"
      @click="handleClickSearchBar"
    >
      <template v-slot:append>
        <q-btn :ripple="false" flat round icon="search" @click="focusFirstLocation()" />
      </template>
    </q-input>
    <q-menu no-focus no-refocus ref="inputMenu" v-model="showMenu" anchor="bottom middle" self="top middle" fit>
      <q-list v-show="orderedLocations.length" bordered>
        <q-item v-for="(location, index) in orderedLocations" :key="index" @click="focusLocation(location)" clickable>
          <q-item-section avatar>
            <q-icon color="primary" name="place" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ location.label }}</q-item-label>
            <q-item-label caption lines="1"><span class="text-caption text-grey">{{ location.renderType() }}</span></q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-menu>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, watch } from 'vue'
import axios from 'axios'
import Location from 'src/api/locations/Location'
import { getLocationPriority } from 'src/api/locations/LocationType'
import { map } from 'src/pages/Index.vue'
import { Map } from 'maplibre-gl'
import { QMenu } from 'quasar'

export default defineComponent({
  setup () {
    const searchInputValue = ref<string | null>(null)
    const emptySearchInput = computed(() => !(searchInputValue.value && searchInputValue.value?.trim().length))
    const locations = ref<Location[]>([])
    const searchIndex = ref<number>(-1)
    const showMenu = ref<boolean>(false)
    const inputMenu = ref<QMenu>()

    const fetchLocations = async () => {
      const fetchMenu = !!searchInputValue.value && !emptySearchInput.value
      showMenu.value = fetchMenu
      searchIndex.value += 1
      const currentSearchIndex = searchIndex.value
      if (fetchMenu) {
        const res = await axios.get('https://api-adresse.data.gouv.fr/search/', {
          params: { q: searchInputValue.value, limit: 5 }
        })
        if (currentSearchIndex === searchIndex.value) {
          locations.value = Location.createFromApi(res)
        }
      } else {
        locations.value = []
      }
    }

    const orderedLocations = computed(() => {
      const res = [...locations.value]
      res.sort((a, b) => getLocationPriority(b.type) - getLocationPriority(a.type))
      return res
    })

    const focusFirstLocation = () => {
      if (orderedLocations.value.length) {
        focusLocation(orderedLocations.value[0])
      }
    }

    const focusLocation = (location: Location) => {
      showMenu.value = false
      inputMenu.value?.hide()
      searchInputValue.value = location.label;
      (map as Map).flyTo({
        center: location.coordinates,
        zoom: 12,
        maxDuration: 3000
      })
    }

    watch(searchInputValue, fetchLocations)

    const handleClickSearchBar = () => {
      if (orderedLocations.value) { inputMenu.value?.show() }
    }

    return {
      searchInputValue,
      locations,
      orderedLocations,
      focusLocation,
      focusFirstLocation,
      handleClickSearchBar,
      showMenu,
      inputMenu
    }
  }
})
</script>

<style lang="scss">
#home-search-bar {
  border-radius: 10px;
  background: white;
  overflow: hidden;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
}
</style>
