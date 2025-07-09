<template>
  <div class="user-info-container">
    <h3>个人信息</h3>
    <table class="user-info-table">
      <tbody>
        <tr>
          <td>头像</td>
          <td><img :src="avatarUrl" alt="用户头像" class="user-avatar" /></td>
          <td>昵称</td>
          <td>{{ userName }}</td>
        </tr>
        <tr>
          <td>性别</td>
          <td>{{ gender }}</td>
          <td>位置</td>
          <td>{{ location }}</td>
        </tr>
        <tr>
          <td>身高 (cm)</td>
          <td>{{ height }}</td>
          <td>体重 (kg)</td>
          <td>{{ weight }}</td>
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
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'UserInfo2',
  props: {
    avatarUrl: String,
    userName: String,
    gender: String,
    location: String,
    height: String,
    weight: String,
    email: String,
    phonenumber: String,
    personalNote: String,
    registrationDate: String
  }
};
</script>


<style scoped src="@/assets/styles/UserInfo2.css"></style>
