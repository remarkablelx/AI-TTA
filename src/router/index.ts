import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import MainView from "@/views/MainView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ChangePasswordView from "@/views/ChangePasswordView.vue";
import History from "@/components/Main/History.vue";

import UserInfo2 from "@/components/Main/UserInfo2.vue";
import UserInfo3 from "@/components/Main/UserInfo3.vue";
import AnalysisTabs from "@/components/Main/AnalysisTabs.vue";
import FramePanel from "@/components/Main/FramePanel.vue";
import VideoComparator from "@/components/Main/VideoComparator.vue";
import Analysis from "@/components/Main/Analysis.vue";
import AdminLogin from "@/components/Admin/AdminLogin.vue";
import Admin from "@/components/Admin/Admin.vue";
import VideoControls from "@/components/Main/VideoControls.vue";
import Video from "@/components/Main/Video.vue";
import AdminBar from "@/components/Admin/AdminBar.vue";
import UserManagement from "@/components/Admin/UserManagement.vue";
import Visualization from "@/components/Main/Visualization.vue";

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
    },
    {
      path:'/1',
      name:'1',
      component: Visualization
    },
    {
      path:'/2',
      name:'2',
      component: VideoControls
    },
    {
      path:'/adminLogin',
      name:'adminLogin',
      component: AdminLogin
    },
    {
      path:'/admin',
      name:'admin',
      component: Admin
    },
    {
      path:'/adminuser',
      name:'adminuser',
      component: UserManagement
    }
  ],
})

export default router



