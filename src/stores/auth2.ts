// @/stores/auth.ts
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,  // 用户是否已登录
    userInfo: {
      nickname: '',  // 用户昵称
      avatar: '',    // 用户头像
      token: '',     // 用户 token
      user_id: '',   // 用户 ID
    }
  }),
  actions: {
    // 设置用户信息
    setUserInfo(userInfo: { nickname: string, avatar: string, token: string, user_id: string }) {
      this.isAuthenticated = true;
      this.userInfo = userInfo;
    },

    // 清除用户信息
    clearUserInfo() {
      this.isAuthenticated = false;
      this.userInfo = {
        nickname: '',
        avatar: '',
        token: '',
        user_id: ''
      };
    },
  },
});
