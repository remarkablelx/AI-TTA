import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// ✅ 导入并创建 pinia 实例
import { createPinia } from 'pinia'
const app = createApp(App)
const pinia = createPinia()


app.use(router)
app.use(pinia)
app.mount('#app')
