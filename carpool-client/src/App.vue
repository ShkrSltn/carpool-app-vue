<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/login">Вход</RouterLink>
      <RouterLink to="/register">Регистрация</RouterLink>
      <RouterLink to="/map">Карта поездок</RouterLink>
      <RouterLink to="/google-map">Google Карта</RouterLink>
      <RouterLink to="/create-ride">Создать поездку</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>
