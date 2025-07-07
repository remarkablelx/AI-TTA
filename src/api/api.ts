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

// 用户密码登录API
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


// 用户验证码登录API
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

// 用户密码登录API
export const adminLogin = async (account: string, password: string,) => {
try {
    const response = await api.post('/admin/login', {
      account,
      password,
    });
    return response.data;
  } catch (error) {
    throw new Error('密码登录请求失败');
  }
};

// 获取个人信息API
export const get_personalInfo = async (user_id: number) => {
  try {
    // 发起 POST 请求
    const response = await api.post('/user/get_personal_info', {
      user_id,  // 传递 token 参数
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


// 修改个人信息的 API
export const update_personalInfo = async (user_id: number, nickname:string,avatar:string,sex:number,email:string,note:string,height:string,weight:string,location:string) => {
  try {
    // 发起 POST 请求
    const response = await api.post('/user/set_personal_info', {
      user_id,        // 传递 token 参数
      nickname,
      avatar,
      sex,
      email,
      note,
      height,
      weight,
      location
    });
    // 处理返回的数据
    if (response.data) {
      console.log('修改成功:', response.data);
      return response.data;  // 返回修改后的用户信息或其他成功标识
    } else {
      console.error('修改失败');
    }
  } catch (error) {
    console.error('修改个人信息时出错:', error);
    throw error;
  }
};

// 注销账户的 API
export const cancel_account = async (user_id: number, captcha_id: string, smsCode: string) => {
  try {
    // 发起 POST 请求
    const response = await api.post('/user/cancel_account', {
      user_id,
      captcha_id,
      captcha_text: smsCode,  // 提交用户输入的验证码
    });
    // 处理返回的数据
    if (response.data) {
      console.log('注销成功:', response.data);
      return response.data;
    } else {
      console.error('注销失败');
    }
  } catch (error) {
    console.error('注销个人信息时出错:', error);
    throw error;
  }
};

// 修改密码的 API
export const set_password = async (user_id: number, new_password:string, captcha_id: string, smsCode: string) => {
  try {
    // 发起 POST 请求
    const response = await api.post('/user/set_password', {
      user_id,
      new_password,
      captcha_id,
      captcha_text: smsCode,  // 提交用户输入的验证码
    });
    // 处理返回的数据
    if (response.data) {
      console.log('重置成功:', response.data);
      return response.data;
    } else {
      console.error('重置失败');
    }
  } catch (error) {
    console.error('重置时出错:', error);
    throw error;
  }
};


// 获取历史记录的API
export const get_allRecord = async (user_id:number,page_num:number,page_size:number) => {
try {
    const response = await api.post('/record/all_record', {
      user_id,
      page_num,
      page_size
    });
    console.log(response);
    return response.data;
  } catch (error) {
    throw new Error('历史记录请求失败');
  }
};

// 新增历史记录的API
export const add_record = async (video_id: number,user_id:number) => {
try {
    const response = await api.post('/record/add_record', {
      video_id,
      user_id,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    throw new Error('增填记录请求失败');
  }
};

// 查看单个分析记录
export const get_record = async (record_id:number) => {
try {
    const response = await api.post('/record/get_record', {
      record_id,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    throw new Error('查看单个记录请求失败');
  }
};

// 修改分析记录
export const set_record = async (record_id:number,state:number,video_name:string,expiration_time:string) => {
try {
    const response = await api.post('/record/set_record', {
      record_id,
      state,
      video_name,
      expiration_time,
    });
    return response.data;
  } catch (error) {
    throw new Error('修改分析记录请求失败');
  }
};

// 删除分析记录
export const delete_record = async (record_id:number) => {
try {
    const response = await api.post('/record/delete_record', {
      record_id,
    });
    return response.data;
  } catch (error) {
    throw new Error('删除分析记录请求失败');
  }
};

// 筛选分析记录
export const search_record = async (user_id:number,search:string,state:number,sort:string,page_num:number,page_size:number) => {
try {
    const response = await api.post('/record/search_record', {
      user_id,
      search,
      state,
      sort,
      page_num,
      page_size,

    });
    return response.data;
  } catch (error) {
    console.log('筛选分析记录请求失败'+error)
    throw new Error('筛选分析记录请求失败');
  }
};

// 获取视频的API
export const uploadVideo = async (video_path:string,video_name:string) => {
try {
    const response = await api.post('/video/upload_video', {
      video_path,
      video_name
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    throw new Error('视频请求失败');
  }
};
