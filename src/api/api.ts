import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://192.168.223.250:5000', // 后端接口基础 URL
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
    console.log("原回复是："+response);
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


// 管理员登录API
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

//查看用户列表API
export const get_allUser = async (page_num:number,page_size:number) => {
try {
    const response = await api.post('/admin/all_user', {
      page_num,
      page_size
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.log('查看用户列表请求失败'+error)
    throw new Error('查看用户列表请求失败');
  }
};


// 查看用户详细信息
export const get_user_info = async (user_id:number) => {
try {
    const response = await api.post('/admin/get_user_info', {
      user_id,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.log('查看用户详细信息请求失败'+error)
    throw new Error('查看用户详细信息失败');
  }
};

// 删除用户
export const delete_user = async (user_id:number) => {
try {
    const response = await api.post('/admin/delete_user', {
      user_id,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.log('删除用户请求失败'+error)
    throw new Error('删除用户失败');
  }
};

// 筛选用户
export const filter_user = async (search:string,sort:string,order:string,sex:number,page_num:number,page_size:number) => {
try {
    const response = await api.post('/admin/filter_user', {
      search,
      sort, // 要排序的字段
      order, // 排序方式
      sex,  // 性别筛选
      page_num, //当前页面号
      page_size, //页面大小

    });
    return response.data;
  } catch (error) {
    console.log('筛选分析记录请求失败'+error)
    throw new Error('筛选分析记录请求失败');
  }
};



//查看用户列表API
export const AdminGetAllRecord = async (page_num:number,page_size:number) => {
try {
    const response = await api.post('/admin/all_record', {
      page_num,
      page_size
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.log('查看分析记录列表请求失败'+error)
    throw new Error('查看分析记录列表请求失败');
  }
};

// 删除记录
export const AdminDeleteRecord = async (record_id:number) => {
try {
    const response = await api.post('/admin/delete_record', {
      record_id,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.log('删除记录请求失败'+error)
    throw new Error('删除记录失败');
  }
};


// 筛选记录
export const filter_record = async (search:string,order:string,state:number,page_num:number,page_size:number) => {
try {
    const response = await api.post('/admin/filter_record', {
      search,
      order, // 按照时间顺序排序
      state,  // 状态筛选
      page_num, //当前页面号
      page_size, //页面大小
    });
    return response.data;
  } catch (error) {
    console.log('筛选所有用户的分析记录请求失败'+error)
    throw new Error('筛选所有用户的分析记录请求失败');
  }
};



// 上传视频
export const uploadVideo = async (video_file: File, video_name: string) => {
  try {
    const formData = new FormData();
    formData.append('video_file', video_file); // 添加视频文件
    formData.append('video_name', video_name); // 添加视频名称

    const response = await api.post('/video/upload_video', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // 确保请求以 multipart 形式发送
      }
    });

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.log("视频上传失败"+error)
    throw new Error('视频请求失败');
  }
};


// 生成分析结果 API
export const generate_result = async (record_id:number) => {
try {
    const response = await api.post('/result/generate_result', {
      record_id
    });
    return response.data;
  } catch (error) {
    console.log('生成分析结果请求失败'+error)
    throw new Error('生成分析结果请求失败');
  }
};

// 查看视频分析结果API
export const get_result = async (result_id:number) => {
try {
    console.log("当前的get_result_result_id是"+result_id)
    const response = await api.post('/result/get_result', {
      result_id
    });
    return response.data;
  } catch (error) {
    console.log('查看视频分析请求失败'+error)
    throw new Error('查看视频分析请求失败');
  }
};

// 获取视频API
export const get_video = async (video_path: string) => {
  try {
    const response = await api.post('/result/get_video', {
      video_path
    }, { responseType: 'blob' }); // 确保后端返回视频文件 (Blob)
    return response.data;
  } catch (error) {
    console.log('获取视频请求失败' + error);
    throw new Error('获取视频请求失败');
  }
};

// 获取JSON文件API
export const get_json = async (json_path: string) => {
  try {
    const response = await api.post('/result/get_json', {
      json_path
    } );
    return response.data;
  } catch (error) {
    console.log('获取json请求失败' + error);
    throw new Error('获取json请求失败');
  }
};

// 获取分析报告API
export const create_report = async (result_id:number) => {
try {
    console.log("当前的get_result是"+result_id)
    const response = await api.post('/report/create_report', {
      result_id
    });
    return response.data;
  } catch (error) {
    console.log('生成分析报告请求失败'+error)
    throw new Error('生成分析报告请求失败');
  }
};

// 查看分析报告API
export const view_report = async (report_id:number) => {
try {
    console.log("当前的report_id是"+report_id)
    const response = await api.post('/report/get_report', {
      report_id
    });
    return response.data;
  } catch (error) {
    console.log('查看分析报告请求失败'+error)
    throw new Error('查看分析报告请求失败');
  }
};

// 删除分析报告API
export const delete_report = async (report_id
:number) => {
try {
    console.log("当前的report_id是"+report_id)
    const response = await api.post('/report/delete_report', {
      report_id
    });
    return response.data;
  } catch (error) {
    console.log('查看分析报告请求失败'+error)
    throw new Error('查看分析报告请求失败');
  }
};
