<script setup>
import Home from "@/components/Home/Home.vue"
import CoreTech from "@/components/Home/CoreTech.vue";
</script>

<template>
  <div class="container">
    <Home />
    <CoreTech />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column; /* 垂直排列 */
  width: 100vw; /* 横向撑满整个浏览器页面 */
}

.container > * {
  width: 100%; /* 每个子组件横向撑满容器 */
}
</style>
