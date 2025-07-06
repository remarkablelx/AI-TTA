// stores/userStore.js
import { defineStore } from 'pinia';


export const useUserStore = defineStore('user', {
  state: () => ({
    token: '',         // 用来存储 token
    isLoggedIn: false, // 用来表示用户是否登录
    userInfo: {
      user_id: 0,               // 用户 ID
      account: '',              // 用户账号
      nickname: '',             // 用户昵称
      avatarUrl: '',            // 用户头像 URL
      userName: '',             // 用户姓名
      gender: 0,                // 用户性别，0为女，1为男
      height: '',               // 用户身高
      weight: '',               // 用户体重
      email: '',                // 用户邮箱
      location: '',             // 用户位置
      personalNote: '',         // 用户个人说明
      registrationDate: ''      // 用户注册日期
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
    setUserInfo(user_id: number, account: string, nickname: string, avatar: string) {
      this.userInfo.user_id=user_id;
      this.userInfo.account=account;
      this.userInfo.nickname=nickname;
      this.userInfo.avatarUrl=avatar;
    },
  },
});
