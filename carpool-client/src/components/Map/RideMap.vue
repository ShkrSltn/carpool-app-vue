<template>
    <div class="ride-map">
      <div class="search-controls">
        <div class="search-input">
          <input 
            ref="originInput"
            type="text" 
            placeholder="Откуда"
            v-model="origin"
          >
        </div>
        <div class="search-input">
          <input 
            ref="destinationInput"
            type="text" 
            placeholder="Куда"
            v-model="destination"
          >
        </div>
      </div>
      
      <div id="map" ref="mapDiv" style="height: 400px; width: 100%;"></div>
      
      <div v-if="distance" class="route-info">
        <p>Расстояние: {{ distance }}</p>
        <p>Время в пути: {{ duration }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { Loader } from '@googlemaps/js-api-loader'
  
  const mapDiv = ref(null)
  const originInput = ref(null)
  const destinationInput = ref(null)
  const origin = ref('')
  const destination = ref('')
  const distance = ref('')
  const duration = ref('')
  
  const loader = new Loader({
    apiKey: 'AIzaSyC1ZuTJZcheQBfERhE7S1EPIsKq76CIFuM',
    version: 'weekly',
    libraries: ['places']
  })
  
  onMounted(async () => {
    try {
      const google = await loader.load()
      const map = new google.maps.Map(mapDiv.value, {
        center: { lat: 47.0270, lng: 8.6526 },
        zoom: 12
      })
  
      const directionsService = new google.maps.DirectionsService()
      const directionsRenderer = new google.maps.DirectionsRenderer({
        map: map
      })
  
      // Инициализация автозаполнения
      const originAutocomplete = new google.maps.places.Autocomplete(originInput.value)
      const destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput.value)
  
      // Слушатели событий для автозаполнения
      originAutocomplete.addListener('place_changed', () => calculateRoute())
      destinationAutocomplete.addListener('place_changed', () => calculateRoute())
  
      // Функция расчета маршрута
      function calculateRoute() {
        const originPlace = originAutocomplete.getPlace()
        const destinationPlace = destinationAutocomplete.getPlace()
  
        if (!originPlace || !destinationPlace) return
  
        const request = {
          origin: originPlace.geometry.location,
          destination: destinationPlace.geometry.location,
          travelMode: google.maps.TravelMode.DRIVING
        }
  
        directionsService.route(request, (result, status) => {
          if (status === 'OK') {
            directionsRenderer.setDirections(result)
            
            // Обновление информации о маршруте
            const route = result.routes[0]
            distance.value = route.legs[0].distance.text
            duration.value = route.legs[0].duration.text
          }
        })
      }
  
    } catch (error) {
      console.error('Error loading Google Maps:', error)
    }
  })
  </script>
  
  <style scoped>
  .ride-map {
    padding: 20px;
  }
  
  .search-controls {
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
  }
  
  .search-input {
    flex: 1;
  }
  
  .search-input input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .route-info {
    margin-top: 20px;
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
  </style>