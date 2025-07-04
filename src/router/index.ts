import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import MainView from "@/views/MainView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ChangePasswordView from "@/views/ChangePasswordView.vue";
import History from "@/components/Main/History.vue";
import Video from"@/components/Main/AnalysisVideo.vue"
import UserInfo2 from "@/components/Main/UserInfo2.vue";
import UserInfo3 from "@/components/Main/UserInfo3.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path:'/register',
      name:'register',
      component: RegisterView
    },
    {
      path:'/change',
      name:'change',
      component: ChangePasswordView
    },
    {
      path:'/main',
      name:'main',
      component: MainView
    },
    {
      path:'/history',
      name:'history',
      component:History
    },
    {
      path:'/userinfo',
      name:'userinfo',
      component: UserInfo3
    }
  ],
})

export default router



