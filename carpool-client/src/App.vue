<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <Registration />
      <RouterLink to="/login">Вход</RouterLink>
      <RouterLink to="/register">Регистрация</RouterLink>
      <RouterLink to="/map">Карта поездок</RouterLink>
      <RouterLink to="/google-map">Google Карта</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>
