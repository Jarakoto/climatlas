<template>
  <div
    @keydown="handleKeyDown"
    @click="focusInput"
    v-click-outside="unfocusInput"
    @mouseover="isBarHovered = true"
    @mouseleave="isBarHovered = false"
    :class="`search-location-bar ${isMenuDisplayed ? 'menu-displayed' : ''}`"
  >
    <v-text-field
      hide-details
      ref="searchTextField"
      density="compact"
      id="searchTextField"
      append-icon="mdi-magnify"
      label="Rechercher un lieu ou une adresse"
      v-model="stringSearch"
      class="pa-2 search-text-field"
      @focus="indexFocusedOption = -1"
    />
    <div class="px-4">
      <v-divider v-if="isMenuDisplayed" />
    </div>
    <div class="search-results-container" v-if="isMenuDisplayed">
      <v-list density="compact" class="search-results">
        <!-- <SearchResultVue
      v-for="(location, index) in foundLocations"
      :index="index"
      :location="(location as LocationResult)"
      :stringSearch="stringSearch"
      ref="locationsRefs"
      @focus="indexFocusedOption = index"
    /> -->
      </v-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NitroFetchRequest } from "nitropack";
// import { SEARCH_PARCEL_URL } from "~/constants/api";
// import { LocationResult } from "~/api/locationsSearch/locationSearch.classes";
// import { ValidationKey } from "~/api/validation/ValidationKey";
// import ValidationManager from "~/api/validation/ValidationManager";
import SearchResultVue from "./SearchResult.vue";

const config = useRuntimeConfig();

const indexFocusedOption = ref(-1);
const isInputFocused = ref(false);
const isBarHovered = ref(false);
const stringSearch = ref("");
const locationsRefs = ref([]);

const nextSearch = ref(null as string | null);
const foundLocations = ref([] as LocationResult[]);
const querySearchLoading = ref(false);

const findLocations = async () => {
  // querySearchLoading.value = true;
  // if (!nextSearch.value) {
  //   nextSearch.value = stringSearch.value;
  // }
  // const currentSearch = stringSearch.value.slice();
  // const res = await $fetch(
  //   `${SEARCH_PARCEL_URL(config)}?searchItem=${currentSearch}` as NitroFetchRequest
  // );
  // try {
  //   ValidationManager.validate(ValidationKey.LOCATION_RESULTS, res);
  // } catch (err) {
  //   throw err;
  // } finally {
  //   setTimeout(() => {
  //     if (nextSearch.value == null) {
  //       querySearchLoading.value = false;
  //     }
  //   }, 300);
  //   if (currentSearch === nextSearch.value) {
  //     nextSearch.value = null;
  //     foundLocations.value = res as LocationResult[];
  //   } else {
  //     findLocations();
  //   }
  // }
};

watch(stringSearch, async (newValue) => {
  if (newValue.trim().length > 0) {
    if (!nextSearch.value) {
      findLocations();
    } else {
      console.log("go");
      nextSearch.value = newValue;
    }
  }
});

const locationsExists = computed(() => {
  return !!foundLocations.value && !!foundLocations.value.length;
});

const isMenuDisplayed = computed(() => {
  return isInputFocused.value && locationsExists.value && stringSearch.value.length;
});

const elevatedBar = computed(() => {
  return isMenuDisplayed.value || isBarHovered.value;
});

const focusInput = () => {
  isInputFocused.value = true;
};

const unfocusInput = () => {
  isInputFocused.value = false;
};

const focusSearchTextField = () => {
  document.getElementById("searchTextField")?.click();
};

const handleKeyDown = (event) => {
  const keyCode = event.keyCode;
  if (locationsExists.value && foundLocations.value.length) {
    if (keyCode === 40) {
      if (indexFocusedOption.value === foundLocations.value.length - 1) {
        indexFocusedOption.value = -1;
        focusSearchTextField();
      } else {
        indexFocusedOption.value += 1;
        // locationsRefs.value[indexFocusedOption.value].$el.focus();
      }
    } else if (keyCode === 38) {
      if (foundLocations.value.length) {
        if (indexFocusedOption.value === -1) {
          indexFocusedOption.value = foundLocations.value.length - 1;
        } else {
          indexFocusedOption.value -= 1;
        }
        if (indexFocusedOption.value !== -1) {
          // locationsRefs.value[indexFocusedOption.value].$el.focus();
        } else {
          focusSearchTextField();
        }
      }
    }
  }
};
</script>

<style lang="scss">
.invis-activator {
  height: 0 !important;
  opacity: 0 !important;
  box-shadow: none;
}

.search-location-bar {
  background: #fff;
  border: 1px solid #dfe1e5;
  box-shadow: none;
  border-radius: 8px;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);

  .query-loader {
    height: 56px;
    position: absolute;
    top: 0;
    right: -2rem;
  }

  &.menu-displayed {
    border-bottom: 0px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .search-text-field {
    z-index: 4;
    width: 100%;
    box-sizing: border-box;
  }

  .v-field__outline {
    display: none !important;
  }
  position: relative;
  .v-field {
    border-radius: 0 !important;
  }

  .v-field__overlay {
    background: none !important;
  }

  .v-field__append-inner {
    display: none; // TOREMOVE When Vuetify update
  }
  .v-field__input {
    // TOREMOVE When Vuetify update
    input {
      width: 100%;
    }
  }
}
</style>
