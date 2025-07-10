import { createRouter, createWebHistory } from 'vue-router'
import HomeView from "@/views/Home/HomeView.vue";
import LoginView from "@/views/Users/LoginView.vue";
import MainView from "@/views/Main/MainView.vue";
import RegisterView from "@/views/Users/RegisterView.vue";
import ChangePasswordView from "@/views/Users/ChangePasswordView.vue";
import History from "@/components/Main/History/History.vue";
import AdminLogin from "@/components/Admin/AdminLogin.vue";
import AdminView from "@/views/Admin/AdminView.vue";
import { useUserStore } from '@/stores/userStore';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false } // 首页不需要认证
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false } // 登录页不需要认证
    },
    {
      path:'/register',
      name:'register',
      component: RegisterView,
      meta: { requiresAuth: false } // 注册页不需要认证
    },
    {
      path:'/change',
      name:'change',
      component: ChangePasswordView,
      meta: { requiresAuth: false } // 修改密码不需要认证
    },
    {
      path:'/main',
      name:'main',
      component: MainView,
      meta: { requiresAuth: true } // 主页面需要认证
    },
    {
      path:'/history',
      name:'history',
      component: History,
      meta: { requiresAuth: true } // 历史记录需要认证
    },
    {
      path:'/adminLogin',
      name:'adminLogin',
      component: AdminLogin,
      meta: { requiresAuth: false } // 管理员登录不需要认证
    },
    {
      path:'/admin',
      name:'admin',
      component: AdminView,
      meta: { requiresAuth: false} // 管理员页面需要认证和admin权限
    },
  ],
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const isAuthenticated = userStore.userInfo.user_id > 0;

  // 如果路由需要认证但用户未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  }
  // 如果用户已登录但尝试访问登录/注册页
  else if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    next({ name: 'home' });
  }
  // 其他情况允许访问
  else {
    next();
  }
});

export default router