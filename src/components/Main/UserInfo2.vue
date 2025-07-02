<template>
  <div class="user-info-container">
    <h3>个人信息</h3>

    <!-- 个人信息表格 -->
    <table class="user-info-table">
      <tr>
        <td>头像</td>
        <td><img :src="avatarUrl" alt="用户头像" class="user-avatar" /></td>
        <td>昵称</td>
        <td>{{ userName }}</td>
      </tr>
      <tr>
        <td>性别</td>
        <td>{{ gender }}</td>
        <td>身高 (cm)</td>
        <td>{{ height }}</td>
      </tr>
      <tr>
        <td>体重 (kg)</td>
        <td>{{ weight }}</td>
        <td>BMI</td>
        <td>{{ bmi }}</td>
      </tr>
      <tr>
        <td>邮箱</td>
        <td>{{ email }}</td>
        <td>电话号码</td>
        <td>{{ phonenumber }}</td>
      </tr>
      <tr>
        <td>个人说明</td>
        <td colspan="3">{{ personalNote }}</td>
      </tr>
      <tr>
        <td>注册时间</td>
        <td colspan="3">{{ registrationDate }}</td>
      </tr>
    </table>

    <!-- 编辑表单弹窗 -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <h3>编辑个人信息</h3>
        <form @submit.prevent="handleSubmit">
          <div class="modal-row">
            <label>头像 URL</label>
            <input type="text" v-model="form.avatarUrl" />
          </div>
          <div class="modal-row">
            <label>昵称</label>
            <input type="text" v-model="form.userName" />
          </div>
          <div class="modal-row">
            <label>性别</label>
            <select v-model="form.gender">
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="modal-row">
            <label>身高 (cm)</label>
            <input type="number" v-model="form.height" min="0" />
          </div>
          <div class="modal-row">
            <label>体重 (kg)</label>
            <input type="number" v-model="form.weight" min="0" />
          </div>
          <div class="modal-row">
            <label>邮箱</label>
            <input type="email" v-model="form.email" />
          </div>
          <div class="modal-row">
            <label>电话号码</label>
            <input type="text" v-model="form.phonenumber" />
          </div>
          <div class="modal-row">
            <label>个人说明</label>
            <textarea v-model="form.personalNote"></textarea>
          </div>
          <div class="modal-row">
            <label>注册时间</label>
            <input type="text" v-model="form.registrationDate" disabled />
          </div>
          <button type="submit">提交</button>
          <button type="button" @click="closeModal">关闭</button>
        </form>
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
      avatarUrl: 'https://link-to-avatar.jpg',
      userName: 'jack',
      gender: '男',
      height: 175,
      weight: 70,
      email: 'jack@example.com',
      phonenumber: '19132050485',
      personalNote: '这是个人说明',
      registrationDate: '2022-01-26 16:29:44',
      // 编辑表单的数据
      form: {
        avatarUrl: 'https://link-to-avatar.jpg',
        userName: 'jack',
        gender: '男',
        height: 175,
        weight: 70,
        email: 'jack@example.com',
        phonenumber: '19132050485',
        personalNote: '这是个人说明',
        registrationDate: '2022-01-26 16:29:44',
      }
    };
  },
  computed: {
    bmi() {
      const heightInMeters = this.height / 100;
      return (this.weight / (heightInMeters * heightInMeters)).toFixed(2);
    }
  },
  methods: {
    // 提交编辑表单
    handleSubmit() {
      this.avatarUrl = this.form.avatarUrl;
      this.userName = this.form.userName;
      this.gender = this.form.gender;
      this.height = this.form.height;
      this.weight = this.form.weight;
      this.email = this.form.email;
      this.phonenumber = this.form.phonenumber;
      this.personalNote = this.form.personalNote;
      this.registrationDate = this.form.registrationDate;

      this.showEditModal = false;
    },
    // 关闭弹窗
    closeModal() {
      this.showEditModal = false;
    }
  }
};
</script>

<style scoped>
/* 个人信息容器 */
.user-info-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

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
}

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
  width: 400px;
}

.modal-row {
  margin-bottom: 15px;
}

.modal-row label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.modal-row input,
.modal-row select,
.modal-row textarea {
  width: 100%;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
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
</style>
