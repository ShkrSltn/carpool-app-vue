<template>
  <div>
    <div id="map" ref="mapDiv" style="height: 400px; width: 100%;"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

const mapDiv = ref(null)
const props = defineProps({
  center: {
    type: Object,
    default: () => ({ lat: 55.7558, lng: 37.6173 }) // Москва по умолчанию
  },
  zoom: {
    type: Number,
    default: 12
  }
})

const loader = new Loader({
  apiKey: 'AIzaSyC1ZuTJZcheQBfERhE7S1EPIsKq76CIFuM',
  version: 'weekly',
  libraries: ['places']
})

onMounted(async () => {
  try {
    const google = await loader.load()
    const map = new google.maps.Map(mapDiv.value, {
      center: props.center,
      zoom: props.zoom,
      mapTypeControl: true,
      streetViewControl: true,
      fullscreenControl: true
    })
  } catch (error) {
    console.error('Error loading Google Maps:', error)
  }
})
</script>
