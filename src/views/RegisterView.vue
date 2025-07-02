<script setup lang="ts">
import Register from "@/components/Register/Register.vue";
</script>

<template>
  <div class="body">
    <Register />
  </div>
</template>

<style scoped>
.body {
  height: 100vh;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}
.body {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  width: 100vw; /* 横向撑满整个浏览器页面 */
}

.container > * {
  width: 100%; /* 每个子组件横向撑满容器 */
}
</style>