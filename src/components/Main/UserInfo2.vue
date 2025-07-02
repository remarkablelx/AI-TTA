<template>
  <div class="user-info-container">
    <h3>个人信息</h3>

    <!-- 个人信息表格 -->
    <table class="user-info-table">
      <tbody>
        <tr>
          <td>头像</td>
          <td>
            <img :src="form.avatarUrl" alt="用户头像" class="user-avatar" @click="triggerFileInput"/>
            <input type="file" ref="fileInput" style="display: none;" @change="handleFileUpload" accept="image/*"/>
          </td>
          <td>昵称</td>
          <td>{{ form.userName }}</td>
        </tr>
        <tr>
          <td>性别</td>
          <td>{{ form.gender }}</td>
          <td>身高 (cm)</td>
          <td>{{ form.height }}</td>
        </tr>
        <tr>
          <td>体重 (kg)</td>
          <td>{{ form.weight }}</td>
          <td>BMI</td>
          <td>{{ bmi }}</td>
        </tr>
        <tr>
          <td>邮箱</td>
          <td>{{ form.email }}</td>
          <td>电话号码</td>
          <td>{{ form.phonenumber }}</td>
        </tr>
        <tr>
          <td>个人说明</td>
          <td colspan="3">{{ form.personalNote }}</td>
        </tr>
        <tr>
          <td>注册时间</td>
          <td colspan="3">{{ form.registrationDate }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 编辑按钮 -->
    <div class="edit-button-container">
      <button @click="showEditModal = true">编辑</button>
    </div>

    <!-- 编辑表单弹窗 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>编辑个人信息</h3>
        <form @submit.prevent="handleSubmit">
          <table class="user-info-table">
            <tbody>
              <tr>
                <td>头像</td>
                <td>
                  <img :src="form.avatarUrl" alt="用户头像" class="user-avatar" @click="triggerFileInput"/>
                  <input type="file" ref="fileInput" style="display: none;" @change="handleFileUpload" accept="image/*"/>
                </td>
                <td>昵称</td>
                <td><input type="text" v-model="form.userName" /></td>
              </tr>
              <tr>
                <td>性别</td>
                <td><input type="text" v-model="form.gender" /></td>
                <td>身高 (cm)</td>
                <td><input type="number" v-model="form.height" min="0" /></td>
              </tr>
              <tr>
                <td>体重 (kg)</td>
                <td><input type="number" v-model="form.weight" min="0" /></td>
                <td>BMI</td>
                <td>{{ bmi }}</td>
              </tr>
              <tr>
                <td>邮箱</td>
                <td><input type="email" v-model="form.email" /></td>
                <td>电话号码</td>
                <td><input type="text" v-model="form.phonenumber" /></td>
              </tr>
              <tr>
                <td>个人说明</td>
                <td colspan="3"><textarea v-model="form.personalNote"></textarea></td>
              </tr>
              <tr>
                <td>注册时间</td>
                <td colspan="3"><input type="text" v-model="form.registrationDate" disabled /></td>
              </tr>
            </tbody>
          </table>
          <div class="form-actions">
            <button type="submit">提交</button>
            <button type="button" @click="closeModal">关闭</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 错误弹窗 -->
    <div v-if="errorMessages.length > 0" class="error-modal">
      <div class="error-modal-content">
        <h3>数据输入不规范</h3>
        <ul>
          <li v-for="(msg, index) in errorMessages" :key="index">{{ msg }}</li>
        </ul>
        <button @click="closeErrorModal">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfo2',
  data() {
    return {
      showEditModal: false, // 控制编辑弹窗显示
      form: {
        avatarUrl: '',
        userName: '',
        gender: '',
        height: '',
        weight: '',
        email: '',
        phonenumber: '',
        personalNote: '',
        registrationDate: '',
      },
      errorMessages: [] // 用于存储验证错误信息
    };
  },
  computed: {
    bmi() {
      const heightInMeters = this.form.height / 100;
      return (this.form.weight / (heightInMeters * heightInMeters)).toFixed(2);
    }
  },
  methods: {
    // 提交编辑表单
    handleSubmit() {
      this.errorMessages = []; // 清空错误信息
      // 验证手机号
      if (!/^\d{11}$/.test(this.form.phonenumber)) {
        this.errorMessages.push("电话号码必须是11位数字");
      }

      // 验证性别
      if (this.form.gender !== '男' && this.form.gender !== '女') {
        this.errorMessages.push("性别必须是男或女");
      }

      // 验证邮箱
      if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$/.test(this.form.email)) {
        this.errorMessages.push("邮箱格式必须为 xxx@xxx.com");
      }

      // 如果有错误，显示错误弹窗
      if (this.errorMessages.length > 0) {
        return;
      }

      // 如果没有错误，提交数据
      this.$emit('update-user', { ...this.form });

      // 关闭编辑弹窗
      this.closeModal();
    },

    // 关闭编辑弹窗
    closeModal() {
      this.showEditModal = false;
    },

    // 头像上传
    triggerFileInput() {
      this.$refs.fileInput.click(); // 触发文件上传框
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          this.form.avatarUrl = reader.result;
        };
        reader.readAsDataURL(file);
      }
    },

    // 关闭错误弹窗
    closeErrorModal() {
      this.errorMessages = [];
    }
  }
};
</script>

<style scoped>
/* 用户信息容器 */
.user-info-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* 简要信息部分 */
h3 {
  font-size: 1.5em;
  margin-bottom: 20px;
}

.user-info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.user-info-table td {
  padding: 12px;
  border: 1px solid #ddd;
}

.user-info-table td img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  object-fit: cover;
}

.user-info-table td input,
.user-info-table td select,
.user-info-table td textarea {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

/* 错误弹窗样式 */
.error-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.error-modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  text-align: center;
}

.error-modal-content h3 {
  color: #e53935;
}

.error-modal-content ul {
  text-align: left;
  color: #e53935;
}

.error-modal-content button {
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.error-modal-content button:hover {
  background-color: #e53935;
}

/* 编辑按钮 */
.edit-button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

button[type="button"] {
  background-color: #f44336;
}

button[type="button"]:hover {
  background-color: #e53935;
}

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 800px;
  height: 600px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.form-actions button {
  margin-left: 10px;
}
</style>
