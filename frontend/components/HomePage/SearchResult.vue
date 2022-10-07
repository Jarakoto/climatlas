<template>
  <v-list-item
    :key="index"
    :value="index"
    :href="LocationResult.getLinkToMapplus(location)"
    ref="locationsRefs"
  >
    <v-icon class="mr-3" color="grey">mdi-map-marker</v-icon>
    {{ formattedLocation.prefix.trim() ? `${formattedLocation.prefix}:` : "" }}
    <span v-if="formattedLocation.prefix.trim()" class="mr-1" />
    <span v-html="highlightText(formattedLocation.label)"></span>
    <span class="text-medium-emphasis"> , {{ formattedLocation.suffix }} </span>
  </v-list-item>
</template>

<script setup lang="ts">
import { PropType } from "vue";
import { LocationResult } from "~/api/locationsSearch/locationSearch.classes";

const props = defineProps({
  location: { type: Object as PropType<LocationResult>, required: true },
  index: { type: Number, required: true },
  stringSearch: { type: String, required: true },
});

const formattedLocation = computed(() => {
  return LocationResult.format(props.location);
});

// Highlight the text matching with the input
const highlightText = (text) => {
  const searchedText = props.stringSearch;
  return text.replaceAll(
    searchedText,
    `<span class="highlighted">${searchedText}</span>`
  );
};
</script>

<style lang="scss">
.search-results-container {
  position: absolute;
  box-sizing: content-box;
  z-index: 2;
  width: 100%;

  .search-results {
    width: 100%;
    left: -1px;
    border: 1px solid #dfe1e5;
    border-top: none;
    border-bottom-left-radius: 28px;
    border-bottom-right-radius: 28px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    .highlighted {
      font-weight: bold;
    }
  }
}
</style>
