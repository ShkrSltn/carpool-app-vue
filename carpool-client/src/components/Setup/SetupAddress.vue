<template>
    <div class="setup-page">
      <div class="header">
        <button class="back-button" @click="$router.go(-1)">←</button>
        <h1>Setup Profile</h1>
      </div>
  
      <div class="address-form">
        <h2>Enter your home address</h2>
        <p class="subtitle">You can change it later</p>
  
        <form @submit.prevent="handleSubmit">
          <input
            id="address-input"
            v-model="address"
            type="text"
            placeholder="Enter starting location"
            class="form-input"
            required
          />
  
          <div id="map" ref="mapDiv" class="map-container"></div>
  
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
  
          <button type="submit" class="next-button">Confirm</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { apiService } from '@/services/api.service'
  import { Loader } from '@googlemaps/js-api-loader'
  
  export default {
    name: 'SetupAddress',
    setup() {
      const router = useRouter()
      const error = ref('')
      const address = ref('')
      const mapDiv = ref(null)
      const marker = ref(null)
      const addressData = ref({
        name: 'Home',
        address: '',
        latitude: 47.0270, // Default to Schwyz, Switzerland
        longitude: 8.6526
      })
  
      onMounted(async () => {
        const token = localStorage.getItem('token')
        if (!token) {
          router.push('/login')
          return
        }
  
        const loader = new Loader({
          apiKey: 'AIzaSyC1ZuTJZcheQBfERhE7S1EPIsKq76CIFuM',
          libraries: ['places']
        })
  
        try {
          const google = await loader.load()
          const map = new google.maps.Map(mapDiv.value, {
            center: { lat: addressData.value.latitude, lng: addressData.value.longitude },
            zoom: 12,
            mapTypeControl: true,
            streetViewControl: true,
            fullscreenControl: true
          })
  
          // Create initial marker
          marker.value = new google.maps.Marker({
            map,
            position: { lat: addressData.value.latitude, lng: addressData.value.longitude },
            draggable: true
          })
  
          const input = document.getElementById('address-input')
          const autocomplete = new google.maps.places.Autocomplete(input, {
            types: ['address'],
            fields: [
              'address_components',
              'formatted_address',
              'geometry',
              'name',
              'place_id'
            ],
            componentRestrictions: { country: 'ch' }
          })
          autocomplete.bindTo('bounds', map)
  
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace()
            if (!place.geometry) return
  
            // Update map and marker
            map.setCenter(place.geometry.location)
            map.setZoom(17)
            marker.value.setPosition(place.geometry.location)
  
            // Update address data
            addressData.value = {
              name: 'Home',
              address: place.formatted_address,
              latitude: place.geometry.location.lat(),
              longitude: place.geometry.location.lng()
            }
            address.value = place.formatted_address
          })
  
          // Handle marker drag events
          marker.value.addListener('dragend', (event) => {
            const lat = event.latLng.lat()
            const lng = event.latLng.lng()
  
            // Reverse geocoding
            const geocoder = new google.maps.Geocoder()
            geocoder.geocode({ location: { lat, lng } }, (results, status) => {
              if (status === 'OK' && results[0]) {
                addressData.value = {
                  name: 'Home',
                  address: results[0].formatted_address,
                  latitude: lat,
                  longitude: lng
                }
                address.value = results[0].formatted_address
              }
            })
          })
  
        } catch (err) {
          console.error('Error loading Google Maps:', err)
          error.value = 'Failed to load map'
        }
      })
  
      const handleSubmit = async () => {
        try {
          if (!addressData.value.address) {
            error.value = 'Please select an address from the dropdown or map'
            return
          }
          
          const userId = parseInt(localStorage.getItem('userId'))
          if (!userId || isNaN(userId)) {
            error.value = 'User ID not found. Please log in again.'
            router.push('/login')
            return
          }
  
          await apiService.updateUserAddress(userId, addressData.value)
          router.push('/setup/role')
        } catch (err) {
          error.value = err.response?.data?.detail || 'Failed to update address'
          if (err.response?.status === 401) {
            router.push('/login')
          }
        }
      }
  
      return {
        address,
        error,
        handleSubmit,
        mapDiv
      }
    }
  }
  </script>
  
  <style scoped>
  /* Можно использовать те же стили, что и в SetupPage.vue */
  .setup-page {
    padding: 20px;
  }
  
  .header {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .back-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
  }
  
  .address-form {
    max-width: 500px;
    margin: 0 auto;
  }
  
  .subtitle {
    color: #666;
    margin-bottom: 30px;
  }
  
  .form-input {
    width: 100%;
    padding: 12px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .next-button {
    width: 100%;
    padding: 15px;
    background-color: #000000;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .next-button:hover {
    background-color: #333333;
  }
  
  .error-message {
    color: #dc3545;
    margin-bottom: 15px;
    text-align: center;
  }
  
  .map-container {
    height: 300px;
    width: 100%;
    margin: 15px 0;
    border-radius: 4px;
    overflow: hidden;
  }
  
  @media screen and (max-width: 768px) {
    .setup-page {
      padding: 15px;
    }
  
    .header h1 {
      font-size: 24px;
    }
  
    .address-form {
      max-width: 100%;
    }
  
    .form-input {
      padding: 10px;
      font-size: 14px;
    }
  
    .next-button {
      padding: 12px;
      font-size: 14px;
    }
  
    .subtitle {
      font-size: 14px;
      margin-bottom: 20px;
    }
  
    h2 {
      font-size: 20px;
    }
  }
  </style>