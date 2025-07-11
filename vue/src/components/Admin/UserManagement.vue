<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { get_allUser, delete_user, get_user_info, filter_user } from "@/api/api.ts";

interface User {
  user_id: number;
  nickname: string;
  sex: number;
  account: string;
  register_time: string;
  record_count: number;
  email?: string;
  height?: number;
  weight?: number;
  location?: string;
  note?: string;
}


const users = ref<User[]>([]);
const page_num = ref(1);
const page_size = ref(6);
const showModal = ref(false);
const userDetails = ref<User | null>(null);
const searchQuery = ref("");

// 获取用户列表
const fetchUsers = async (page_num: number, page_size: number) => {
  try {
    const data = await get_allUser(page_num, page_size);
    users.value = data.records;
    // 打印详细信息
    console.log("获取到的用户数据总览:", data);
    console.log("用户列表详情:", JSON.stringify(users.value, null, 2));
    console.table(users.value); // 在浏览器控制台会显示为表格
  } catch (error) {
    console.error('获取用户列表失败:', error);
  }
};

// 查看用户详细信息
const viewUser = async (user_id: number) => {
  try {
    console.log(user_id)
    const data = await get_user_info(user_id);
    console.log(data)
    if (data.code === 0) {
      userDetails.value = data.user_info;
      console.log("userDetails.value是："+userDetails)
      showModal.value = true;
    }
  } catch (error) {
    console.error('查看用户失败:', error);
  }
};

// 关闭模态框
const closeModal = () => {
  showModal.value = false;
};

// 删除用户
const deleteUser = async (user_id: number) => {
  try {
    console.log(user_id)
    alert("正在删除用户"+user_id)
    const response = await delete_user(user_id);
    if (response.code === "0") {
      await fetchUsers(page_num.value, page_size.value);
    }
    alert("用户删除成功"+user_id)
  } catch (error) {
    console.error('用户删除失败:', error);
  }
};

// 搜索用户
const searchUsers = async () => {
  try {
    const data = await filter_user(
      searchQuery.value || "",
      "",
      "",
      0,
      page_num.value,
      page_size.value
    );
    users.value = data.records;
  } catch (error) {
    console.error('搜索用户失败:', error);
  }
};

// 切换分页
const changePage = (newPageNum: number) => {
  if (newPageNum >= 1) {
    page_num.value = newPageNum;
    if (searchQuery.value) {
      searchUsers();
    } else {
      fetchUsers(page_num.value, page_size.value);
    }
  }
};

// 格式化日期
const formatDate = (dateString: string | undefined | null) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString();
};

onMounted(() => {
  fetchUsers(page_num.value, page_size.value);
});
</script>

<template>
  <div class="admin-user-container">
    <h2>用户列表</h2>
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索用户昵称"
        @input="searchUsers"
      />
    </div>

    <!-- 表格容器，包含可滚动的内容 -->
    <div class="table-container">
      <!-- 表格头部 -->
      <div class="table-header">
        <div class="header-item" style="width: 15%">用户名</div>
        <div class="header-item" style="width: 15%">性别</div>
        <div class="header-item" style="width: 25%">电话</div>
        <div class="header-item" style="width: 25%">注册时间</div>
        <div class="header-item" style="width: 10%">记录数</div>
        <div class="header-item" style="width: 15%">操作</div>
      </div>

      <!-- 显示用户列表 -->
      <div v-for="user in users" :key="user.user_id" class="table-row">
        <div class="row-item" style="width: 15%">{{ user.nickname || '-' }}</div>
        <div class="row-item" style="width: 15%">{{ user.sex === 1 ? '男' : '女' }}</div>
        <div class="row-item" style="width: 25%">{{ user.account || '-' }}</div>
        <div class="row-item" style="width: 25%">{{ formatDate(user.register_time) }}</div>
        <div class="row-item" style="width: 10%">{{ user.record_count || 0 }}</div>
        <div class="row-item" style="width: 15%">
          <button class="view-btn" @click="viewUser(user.user_id)">查看</button>
          <button class="delete-btn" @click="deleteUser(user.user_id)">删除</button>
        </div>
      </div>
    </div>

    <!-- 固定的分页 -->
    <div class="fixed-pagination">
      <button @click="changePage(page_num - 1)">上一页</button>
      <span>页码: {{ page_num }}</span>
      <button @click="changePage(page_num + 1)">下一页</button>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-container">
        <div class="modal-header">
          <h3>用户详细信息</h3>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="info-row">
            <span class="info-label">用户名：</span>
            <span class="info-value">{{ userDetails?.nickname || '-' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">性别：</span>
            <span class="info-value">{{ userDetails?.sex === 1 ? '男' : '女' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">电话：</span>
            <span class="info-value">{{ userDetails?.account || '未设置' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">邮箱：</span>
            <span class="info-value">{{ userDetails?.email || '未设置' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">用户ID：</span>
            <span class="info-value">{{ userDetails?.user_id }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">注册时间：</span>
            <span class="info-value">{{ formatDate(userDetails?.register_time) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">身高：</span>
            <span class="info-value">{{ userDetails?.height || '未设置' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">体重：</span>
            <span class="info-value">{{ userDetails?.weight || '未设置' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">位置：</span>
            <span class="info-value">{{ userDetails?.location || '未设置' }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">备注：</span>
            <span class="info-value">{{ userDetails?.note || '无' }}</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="confirm-btn" @click="closeModal">确定</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-user-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 占满整个视口高度 */
  padding: 20px;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
  background-color: #fff;
  overflow: hidden; /* 防止容器滚动 */
}

.search-bar {
  margin: 20px 0;
}

.search-bar input {
  width: 300px;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.table-container {
  flex: 1; /* 占据剩余空间 */
  overflow-y: auto; /* 允许内容滚动 */
  border: 1px solid #eee;
  border-radius: 4px;
}

.table-header, .table-row {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.table-header {
  position: sticky;
  top: 0;
  background-color: #f5f5f5;
  font-weight: bold;
  color: #333;
  z-index: 10;
}

.row-item, .header-item {
  padding: 0 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.view-btn, .delete-btn {
  padding: 4px 8px;
  margin: 0 3px;
  border: none;
  border-radius: 3px;
  font-size: 12px;
  cursor: pointer;
}

.view-btn {
  background: #1890ff;
  color: white;
}

.delete-btn {
  background: #ff4d4f;
  color: white;
}

.fixed-pagination {
  position: sticky;
  bottom: 0;
  padding: 15px 0;
  background-color: #fff;
  border-top: 1px solid #eee;
  margin-top: auto; /* 确保分页固定在底部 */
  text-align: center;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05);
}

.fixed-pagination button {
  margin: 0 10px;
  padding: 5px 15px;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
}

.fixed-pagination button:hover {
  background: #f5f5f5;
}

/* 修改后的模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  width: 500px;
  max-width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  flex: 1;
}

.info-row {
  display: flex;
  margin-bottom: 12px;
  line-height: 1.5;
}

.info-label {
  width: 80px;
  font-weight: bold;
  color: #666;
}

.info-value {
  flex: 1;
  color: #333;
  word-break: break-word;
}

.modal-footer {
  padding: 12px 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.confirm-btn {
  padding: 6px 16px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn:hover {
  background-color: #40a9ff;
}
</style>