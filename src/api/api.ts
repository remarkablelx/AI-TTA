import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/', // 后端接口基础 URL
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

// 获取验证码 ID 和验证码文本的 API
export const getCaptcha = async () => {
  try {
    const response = await api.post('/user/captcha');
    console.log('验证码获取成功111:', response);  // 打印返回的响应
    return response.data;  // 返回包含 captcha_id 和 captcha_text 的数据
  } catch (error) {
    console.error('验证码获取失败:', error);  // 打印错误信息
    throw new Error('验证码获取失败');
  }
};

// 用户注册 API
export const registerUser = async (account: string, password: string, captcha_id: string, smsCode: string) => {
  try {
    const response = await api.post('/user/register', {
      account,
      password,
      captcha_id,
      captcha_text: smsCode,  // 提交用户输入的验证码
    });
    return response.data;
  } catch (error) {
    throw new Error('注册请求失败');
  }
};

// 密码登录API
export const password_loginUser = async (account: string, password: string,) => {
try {
    const response = await api.post('/user/password_login', {
      account,
      password,
    });
    return response.data;
  } catch (error) {
    throw new Error('密码登录请求失败');
  }
};


// 验证码登录API
export const captcha_loginUser = async (account: string, captcha_id: string, smsCode: string) => {
    try {
    const response = await api.post('/user/captcha_login', {
      account,
      captcha_id,
      captcha_text: smsCode,  // 提交用户输入的验证码
    });
    return response.data;
  } catch (error) {
    throw new Error('验证码登录请求失败');
  }
};

export const get_personalInfo = async (token: string) => {
  try {
    // 发起 POST 请求
    const response = await api.post('/user/get_personal_info', {
      token,  // 传递 token 参数
    });
    // 处理返回的数据
    if (response.data) {
      console.log('获取到的个人信息:', response.data);
      return response.data;
    } else {
      console.error('没有获取到个人信息');
    }
  } catch (error) {
    console.error('获取个人信息时出错:', error);
    throw error;
  }
};
