// stores/userStore.js
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',         // 用来存储 token
    isLoggedIn: false, // 用来表示用户是否登录
    userInfo:{
      user_id:0,
      account:'',
      nickname:''
    }
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
    // 设置 userInfo 信息
    setUserInfo(userInfo: { user_id: number, account: string, nickname: string, avatar: string }) {
      this.userInfo = userInfo;
    },
  },
});
