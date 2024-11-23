<template>
  <div class="create-ride">
    <div class="header">
      <router-link to="/" class="back-arrow">←</router-link>
      <h1>Create Ride</h1>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>Starting Point</label>
        <select v-model="selectedStartingPoint">
          <option value="">Select starting point</option>
          <option v-for="place in favouritePlaces" 
                  :key="place.favourite_place_id" 
                  :value="place">
            {{ place.name }} - {{ place.address }}
          </option>
        </select>
      </div>

      <div class="form-group destination-group">
        <label>Destination</label>
        <input
          ref="destinationInput"
          type="text"
          v-model="destination"
          placeholder="Enter destination"
        />
        <div id="map" ref="mapDiv" class="map-container"></div>
        <div v-if="distance" class="route-info">
          <p>Distance: {{ distance }}</p>
          <p>Duration: {{ duration }}</p>
        </div>
      </div>

      <div class="form-group">
        <label>Departure Time</label>
        <input
          type="datetime-local"
          v-model="departureTime"
          required
        />
      </div>

      <div class="form-group">
        <label>Car</label>
        <div v-if="carError" class="error-message">
          {{ carError }}
        </div>
        <div v-if="!userCars.length" class="no-cars-message">
          <p>You need to add a car first</p>
          <router-link to="/setup" class="add-car-link">Add Car</router-link>
        </div>
        <select v-else v-model="selectedCar" required>
          <option value="">Select your car</option>
          <option v-for="car in userCars" 
                  :key="car.id" 
                  :value="car">
            {{ car.make }} {{ car.model }} ({{ car.plate_number }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label>Available Seats</label>
        <select v-model="availableSeats" required>
          <option value="">Select available seats</option>
          <option v-for="n in 4" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <div class="form-group checkbox">
        <input
          type="checkbox"
          id="recurring"
          v-model="isRecurring"
        />
        <label for="recurring">Recurring ride</label>
      </div>

      <button type="submit" 
              class="next-button"
              :disabled="!isFormValid">
        Create Ride
      </button>
    </form>

    <SetupSchedule 
      v-if="showScheduleSetup"
      @back="showScheduleSetup = false"
      @saved="handleScheduleSaved"
    />

    <ScheduleConfirmation 
      v-if="showScheduleConfirmation"
      :schedules="scheduleData.schedules"
      :ride-details="scheduleData.rideDetails"
      @edit="showScheduleSetup = true; showScheduleConfirmation = false"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'
import { apiService } from '@/services/api.service'
import { useRouter } from 'vue-router'
import SetupSchedule from './SetupSchedule.vue'
import ScheduleConfirmation from './ScheduleConfirmation.vue'

export default {
  name: 'CreateRide',
  components: {
    SetupSchedule,
    ScheduleConfirmation
  },
  setup() {
    const router = useRouter()
    const mapDiv = ref(null)
    const destinationInput = ref(null)
    const favouritePlaces = ref([])
    const userCars = ref([
      {
        id: 1,
        make: 'Toyota',
        model: 'Camry',
        plate_number: 'ZH-123-456'
      },
      {
        id: 2,
        make: 'Honda',
        model: 'Civic',
        plate_number: 'BE-789-012'
      }
    ])
    const selectedStartingPoint = ref('')
    const destination = ref('')
    const destinationCoords = ref(null)
    const departureTime = ref('')
    const selectedCar = ref('')
    const availableSeats = ref('')
    const isRecurring = ref(false)
    const distance = ref('')
    const duration = ref('')
    const carError = ref('')
    const showScheduleSetup = ref(false)
    const showScheduleConfirmation = ref(false)
    const scheduleData = ref(null)

    const isFormValid = computed(() => {
      return selectedStartingPoint.value &&
             destination.value &&
             destinationCoords.value &&
             departureTime.value &&
             selectedCar.value &&
             availableSeats.value
    })

    onMounted(async () => {
      try {
        // Fetch user's favorite places
        const placesResponse = await apiService.getFavouritePlaces()
        favouritePlaces.value = placesResponse.data

        // Initialize Google Maps
        await initializeMap()
      } catch (error) {
        console.error('Error initializing:', error)
      }
    })

    const initializeMap = async () => {
      const loader = new Loader({
        apiKey: 'AIzaSyC1ZuTJZcheQBfERhE7S1EPIsKq76CIFuM',
        libraries: ['places']
      })

      try {
        const google = await loader.load()
        const map = new google.maps.Map(mapDiv.value, {
          center: { lat: 47.0270, lng: 8.6526 },
          zoom: 12
        })

        const autocomplete = new google.maps.places.Autocomplete(destinationInput.value, {
          types: ['address'],
          componentRestrictions: { country: 'ch' }
        })

        autocomplete.addListener('place_changed', () => {
          const place = autocomplete.getPlace()
          if (!place.geometry) return

          destinationCoords.value = {
            latitude: place.geometry.location.lat(),
            longitude: place.geometry.location.lng()
          }
          destination.value = place.formatted_address

          // Update map
          map.setCenter(place.geometry.location)
          map.setZoom(15)

          // Calculate route if starting point is selected
          if (selectedStartingPoint.value) {
            calculateRoute(google, map)
          }
        })
      } catch (error) {
        console.error('Error loading Google Maps:', error)
      }
    }

    const calculateRoute = (google, map) => {
      const directionsService = new google.maps.DirectionsService()
      const directionsRenderer = new google.maps.DirectionsRenderer({ map })

      const request = {
        origin: {
          lat: selectedStartingPoint.value.latitude,
          lng: selectedStartingPoint.value.longitude
        },
        destination: {
          lat: destinationCoords.value.latitude,
          lng: destinationCoords.value.longitude
        },
        travelMode: google.maps.TravelMode.DRIVING
      }

      directionsService.route(request, (result, status) => {
        if (status === 'OK') {
          directionsRenderer.setDirections(result)
          const route = result.routes[0]
          distance.value = route.legs[0].distance.text
          duration.value = route.legs[0].duration.text
        }
      })
    }

    const handleSubmit = async () => {
      if (isRecurring.value) {
        showScheduleSetup.value = true
        return
      }
      try {
        const rideData = {
          origin: selectedStartingPoint.value.address,
          origin_latitude: selectedStartingPoint.value.latitude,
          origin_longitude: selectedStartingPoint.value.longitude,
          destination: destination.value,
          destination_latitude: destinationCoords.value.latitude,
          destination_longitude: destinationCoords.value.longitude,
          departure_time: new Date(departureTime.value).toISOString(),
          available_seats: parseInt(availableSeats.value),
          driver_id: parseInt(localStorage.getItem('userId')),
          car_id: selectedCar.value.id
        }

        await apiService.createRide(rideData)
        router.push('/rides')
      } catch (error) {
        console.error('Error creating ride:', error)
      }
    }

    const handleScheduleSaved = (savedSchedules) => {
      showScheduleSetup.value = false
      showScheduleConfirmation.value = true
      scheduleData.value = {
        schedules: savedSchedules,
        rideDetails: {
          origin: selectedStartingPoint.value.address,
          destination: destination.value,
          car: selectedCar.value
        }
      }
    }

    return {
      favouritePlaces,
      userCars,
      selectedStartingPoint,
      destination,
      departureTime,
      selectedCar,
      availableSeats,
      isRecurring,
      distance,
      duration,
      isFormValid,
      handleSubmit,
      mapDiv,
      destinationInput,
      carError,
      showScheduleSetup,
      handleScheduleSaved,
      showScheduleConfirmation,
      scheduleData
    }
  }
}
</script>

<style scoped>
.create-ride {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.back-arrow {
  text-decoration: none;
  font-size: 24px;
  color: #000;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

input[type="text"],
input[type="datetime-local"],
select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f5f5f5;
}

.map-container {
  height: 300px;
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
}

.route-info {
  margin-top: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.checkbox input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.checkbox label {
  cursor: pointer;
}

.next-button {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
  margin-top: 20px;
  cursor: pointer;
}

.next-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.no-cars-message {
  text-align: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
}

.add-car-link {
  display: inline-block;
  margin-top: 10px;
  color: #007bff;
  text-decoration: none;
}

.add-car-link:hover {
  text-decoration: underline;
}

.error-message {
  color: #dc3545;
  margin-bottom: 10px;
  font-size: 14px;
}
</style>
