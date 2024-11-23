<template>
    <div class="schedule-confirmation">
      <div class="header">
        <h2>Your Schedule</h2>
        <p class="subtitle">Here's your regular ride schedule</p>
      </div>
  
      <div class="schedule-summary">
        <div class="route-details">
          <div class="location">
            <label>From:</label>
            <p>{{ rideDetails.origin }}</p>
          </div>
          <div class="location">
            <label>To:</label>
            <p>{{ rideDetails.destination }}</p>
          </div>
          <div class="car-info">
            <label>Car:</label>
            <p>{{ rideDetails.car.make }} {{ rideDetails.car.model }}</p>
          </div>
        </div>
  
        <div class="schedule-grid">
          <div v-for="(schedule, index) in schedules" 
               :key="index"
               class="day-card"
               :class="{ active: schedule.isActive }">
            <h3>{{ days[schedule.day_of_week] }}</h3>
            <template v-if="schedule.isActive">
              <div class="time-slot">
                <span class="time">{{ formatTime(schedule.start_time) }}</span>
                <span class="separator">→</span>
                <span class="time">{{ formatTime(schedule.end_time) }}</span>
              </div>
            </template>
            <template v-else>
              <div class="inactive">Not scheduled</div>
            </template>
          </div>
        </div>
      </div>
  
      <div class="actions">
        <button @click="editSchedule" class="edit-button">Edit Schedule</button>
        <button @click="confirmSchedule" class="confirm-button">Confirm</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  
  export default {
    name: 'ScheduleConfirmation',
    props: {
      schedules: {
        type: Array,
        required: true
      },
      rideDetails: {
        type: Object,
        required: true
      }
    },
    setup(props, { emit }) {
      const router = useRouter()
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  
      const formatTime = (time) => {
        return new Date(`2000-01-01T${time}`).toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        })
      }
  
      const editSchedule = () => {
        emit('edit')
      }
  
      const confirmSchedule = () => {
        router.push('/rides')
      }
  
      return {
        days,
        formatTime,
        editSchedule,
        confirmSchedule
      }
    }
  }
  </script>
  
  <style scoped>
  .schedule-confirmation {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .header {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .subtitle {
    color: #666;
    margin-top: 5px;
  }
  
  .schedule-summary {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .route-details {
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }
  
  .location, .car-info {
    margin-bottom: 10px;
  }
  
  .location label, .car-info label {
    font-weight: 500;
    color: #495057;
    margin-right: 10px;
  }
  
  .schedule-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .day-card {
    background: white;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    border: 1px solid #dee2e6;
  }
  
  .day-card.active {
    border-color: #28a745;
  }
  
  .day-card h3 {
    margin: 0 0 10px 0;
    color: #212529;
  }
  
  .time-slot {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }
  
  .time {
    font-weight: 500;
    color: #495057;
  }
  
  .separator {
    color: #adb5bd;
  }
  
  .inactive {
    color: #adb5bd;
    font-style: italic;
  }
  
  .actions {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-top: 30px;
  }
  
  .edit-button, .confirm-button {
    padding: 12px 30px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
  }
  
  .edit-button {
    background-color: #f8f9fa;
    color: #212529;
  }
  
  .confirm-button {
    background-color: #28a745;
    color: white;
  }
  </style>