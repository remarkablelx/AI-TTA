// stores/userStore.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',         // 用来存储 token
    isLoggedIn: false, // 用来表示用户是否登录
  }),
  actions: {
    // 设置 token 并标记为登录状态
    setToken(token: string) {
      this.token = token;
      this.isLoggedIn = true;
    },
    // 清除 token 并标记为未登录状态
    clearToken() {
      this.token = '';
      this.isLoggedIn = false;
    },
  },
});
