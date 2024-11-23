<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usersApi } from '@/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const name = ref('')
const surname = ref('')
const username = ref('')
const error = ref('')

const register = async () => {
  try {
    const response = await usersApi.register({
      email: email.value,
      username: username.value,
      password: password.value,
      name: name.value,
      surname: surname.value,
      car: {} // Include empty car object
    })
    
    if (response.data) {
      router.push('/login')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 
                  (Array.isArray(err.response?.data) ? err.response.data[0]?.msg : 'Ошибка при регистрации')
  }
}
</script>