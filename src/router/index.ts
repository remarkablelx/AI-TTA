import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import MainView from "@/views/MainView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ChangePasswordView from "@/views/ChangePasswordView.vue";
import UserInfo2 from '@/components/Main/UserInfo2.vue';
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
      path:'/userinfo2',
      name:'userinfo2',
      component:UserInfo2
    }
  ],
})

export default router
