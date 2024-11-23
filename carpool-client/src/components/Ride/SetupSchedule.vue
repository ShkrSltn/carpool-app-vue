<template>
    <div class="schedule-setup">
      <h2>Set Your Regular Schedule</h2>
      <p class="subtitle">Choose days and times when you regularly travel</p>
  
      <div class="days-container">
        <div v-for="(day, index) in days" 
             :key="index" 
             class="day-schedule">
          <div class="day-header">
            <input
              type="checkbox"
              :id="'day-' + index"
              v-model="selectedDays[index]"
            />
            <label :for="'day-' + index">{{ day }}</label>
          </div>
  
          <div v-if="selectedDays[index]" class="time-inputs">
            <div class="time-group">
              <label>Start time:</label>
              <input 
                type="time" 
                v-model="schedules[index].start_time"
                required
              />
            </div>
            <div class="time-group">
              <label>End time:</label>
              <input 
                type="time" 
                v-model="schedules[index].end_time"
                required
              />
            </div>
          </div>
        </div>
      </div>
  
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
  
      <div class="actions">
        <button @click="$emit('back')" class="back-button">Back</button>
        <button @click="saveSchedule" class="save-button">Save Schedule</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue'
  import { apiService } from '@/services/api.service'
  
  export default {
    name: 'SetupSchedule',
    emits: ['back', 'saved'],
    
    setup(props, { emit }) {
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      const selectedDays = ref(Array(7).fill(false))
      const error = ref('')
      
      const schedules = ref(Array(7).fill().map(() => ({
        start_time: '',
        end_time: ''
      })))
  
      const saveSchedule = async () => {
        try {
          const schedulesToSave = selectedDays.value.map((selected, index) => {
            if (!selected) return null
            
            return {
              day_of_week: index,
              start_time: schedules.value[index].start_time,
              end_time: schedules.value[index].end_time
            }
          }).filter(schedule => schedule !== null)
  
          if (schedulesToSave.length === 0) {
            error.value = 'Please select at least one day'
            return
          }
  
          // Save each schedule
          for (const schedule of schedulesToSave) {
            await apiService.createSchedule(schedule)
          }
  
          emit('saved')
        } catch (err) {
          error.value = err.response?.data?.detail || 'Failed to save schedule'
        }
      }
  
      return {
        days,
        selectedDays,
        schedules,
        error,
        saveSchedule
      }
    }
  }
  </script>
  
  <style scoped>
  .schedule-setup {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .subtitle {
    color: #666;
    margin-bottom: 20px;
  }
  
  .days-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .day-schedule {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
  }
  
  .day-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .time-inputs {
    display: flex;
    gap: 20px;
    margin-top: 10px;
  }
  
  .time-group {
    flex: 1;
  }
  
  .time-group label {
    display: block;
    margin-bottom: 5px;
    font-size: 0.9em;
    color: #666;
  }
  
  input[type="time"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .actions {
    display: flex;
    gap: 15px;
    margin-top: 20px;
  }
  
  .back-button,
  .save-button {
    flex: 1;
    padding: 12px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  
  .back-button {
    background-color: #f5f5f5;
    color: #333;
  }
  
  .save-button {
    background-color: #007bff;
    color: white;
  }
  
  .error-message {
    color: #dc3545;
    margin: 10px 0;
    text-align: center;
  }
  </style>