<script setup>
import { useRoute, RouterView } from 'vue-router';

const route = useRoute();
</script>

<template>
  <div id="app">
    <main>
      <RouterView />
    </main>

    <footer v-if="!['/login', '/register'].includes(route.path)" class="footer">
      <nav>
        <RouterLink to="/setup/role">Change Role</RouterLink>
        <RouterLink to="/create-ride">Create a Ride</RouterLink>
      </nav>
    </footer>
  </div>
</template>
