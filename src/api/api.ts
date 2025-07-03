import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://192.168.223.250:5000/', // 后端接口基础 URL
  timeout: 5000, // 请求超时时间
});

// 请求拦截器（如果需要，可以加上 token 或其他头信息）
api.interceptors.response.use(
  response => {
    // 保持完整的 response
    return response;
  },
  error => {
    return Promise.reject(error);
  }
);


// 注册的 API 请求方法
export const registerUser = (account: string, password: string, captcha_id: string, captcha_text: string) => {
  return api.post('/user/register', {
    account,
    password,
    captcha_id,
    captcha_text,
  });
};
// 登录的 API 请求方法
export const loginUser = (account: string, password: string) => {
  return api.post('/user/password_login', {
    account,
    password,
  });
};

