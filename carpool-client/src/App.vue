<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Главная</RouterLink>
      <RouterLink to="/login">Вход</RouterLink>
      <RouterLink to="/register">Регистрация</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped>
nav {
  padding: 20px;
  text-align: center;
}

nav a {
  margin: 0 10px;
  text-decoration: none;
  color: #2c3e50;
}

nav a.router-link-active {
  color: #42b983;
}
</style>
