import './assets/main.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
//  导入并创建 pinia 实例
import { createPinia } from 'pinia'
const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

app.use(router)

app.mount('#app')


