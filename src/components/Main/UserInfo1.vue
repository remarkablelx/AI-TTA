<template>
  <div class="user-info-container">
    <table>
      <tbody>
      <tr>
        <td class="avatar-cell">
          <img :src="avatarUrl" alt="用户头像" />
        </td>
        <td class="info-cell">
          <h3 class="username">{{ userName }}</h3>
          <table class="info-table">
            <tbody> <!-- 添加tbody标签 -->
              <tr>
                <td class="label">性别:</td>
                <td><strong>{{ gender }}</strong></td>
              </tr>
              <tr>
                <td class="label">手机号:</td>
                <td><strong>{{ phonenumber }}</strong></td>
              </tr>
              <tr>
                <td class="label">邮箱:</td>
                <td><strong>{{ email }}</strong></td>
              </tr>
              <tr>
                <td class="label">个人说明:</td>
                <td><strong>{{ personalNote }}</strong></td>
              </tr>
            </tbody> <!-- 结束tbody标签 -->
          </table>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'UserInfo1',
  props: {
    avatarUrl: String,
    userName: String,
    gender: String,
    phonenumber: String,
    email: String,
    personalNote: String
  }
};
</script>

<style scoped src="@/assets/styles/UserInfo1.css"></style>
