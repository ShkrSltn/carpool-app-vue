<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/login">Вход</RouterLink>
      <RouterLink to="/register">Регистрация</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>
