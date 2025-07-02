<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <div id="app">
    <router-view></router-view> <!-- This will render the components based on the route -->
  </div>
</template>

<style scoped>
#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
