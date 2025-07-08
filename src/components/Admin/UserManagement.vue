<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { get_allUser, delete_user, get_user_info, filter_user } from "@/api/api.ts";
import { useUserStore } from "@/stores/userStore.ts";


// 获取 Pinia store
const userStore = useUserStore();


// 示例状态和变量
const users = ref([]); // 存储获取的用户列表
const page_num = ref(1); // 页码
const page_size = ref(6); // 每页条数


// 控制显示用户详情的模态框
const showModal = ref(false); // 控制模态框的显示
const userDetails = ref<any>(null); // 存储获取到的用户详情

// 筛选量
const searchQuery = ref(""); // 搜索框内容
const selectedSex = ref(""); // 默认性别筛选为空
const sortBy = ref<'record_count' | 'register_time' | null>('user_id'); // 排序字段（默认按名称排序）
const sortOrder = ref<'asc' | 'desc'>('asc'); // 排序方式（升序asc，降序desc），默认升序

// 默认搜索框的值
const defaultSearchValue = ""; // 默认值为空，表示所有用户

// 获取用户列表
const fetchUsers = async (page_num: number, page_size: number) => {
  try {
    const data = await get_allUser(page_num, page_size);
    console.log("data.records是"+data.records)
    users.value = data.records; // 假设返回的数据中包含 users
    console.log('获取到的用户列表:', users.value);
  } catch (error) {
    console.error('获取用户列表失败:', error);
  }
};
// 查看用户详细信息
const viewUser = async (user_id: number) => {
  try {
    const data = await get_user_info(user_id);
    if (data.code === "0") {
      console.log('获取信息成功');
      console.log(data)
    }
    userDetails.value = data; // 将返回的用户信息存储到 `userDetails`
    console.log("获得userDetails"+userDetails)
    showModal.value = true; // 显示模态框
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
    const response = await delete_user(user_id); // 向后端发送删除请求
    if (response.code === "0") {
      console.log('用户删除成功');
      await fetchUsers(page_num.value, page_size.value);
    } else {
      console.error('用户删除失败11'+error);
    }
  } catch (error) {
  }
};


// 筛选用户
const searchUsers = async () => {
  try {
    const sex = selectedSex.value === "" ? null : selectedSex.value;
    const sort = sortOrder.value === 'asc' ? sortBy.value + '_asc' : sortBy.value + '_desc';

    const data = await filter_user(searchQuery.value || defaultSearchValue, sort, sortOrder.value, sex, page_num.value, page_size.value);
    console.log(data)

    users.value = data.records;  // 假设返回的数据中包含 users
    console.log('筛选用户成功:', users.value);
  } catch (error) {
    console.error('筛选用户失败:', error);
  }
};


// 切换排序
const toggleSort = (field: 'user_id' | 'record_count' | 'register_time') => {
  if (sortBy.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'; // 切换排序方式
  } else {
    sortBy.value = field; // 设置新的排序字段
    sortOrder.value = 'asc'; // 默认升序
  }
  searchUsers(); // 更新用户列表
};


// 切换分页
const changePage = (newPageNum: number) => {
  if (newPageNum >= 1) {
    page_num.value = newPageNum; // 更新当前页码
    fetchUsers(page_num.value, page_size.value); // 使用当前页码重新加载数据
  }
};




// 组件加载时调用 fetchUsers
onMounted(() => {
  fetchUsers(page_num.value, page_size.value);
});


</script>

<template>
  <div class="container">
    <h2>用户列表</h2>
    <div>
      <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索用户昵称"
          @input="searchUsers"
      />
    </div>

    <!-- 表格头部 -->
    <div class="virtual-header">
      <div class="name-col" @click="toggleSort()">
        <span>用户名</span>
        <span>{{ sortBy === 'name' ? (sortOrder === 1 ? '↑' : '↓') : '' }}</span>
      </div>
      <div>
        <select class="filter-dropdown" v-model="selectedSex" @change="searchUsers">
          <option value=''>性别</option>
          <option value=1>男</option>
          <option value=2>女</option>
        </select>
      </div>
      <div>邮箱</div>
      <div>注册时间</div>
      <div>分析记录数</div>
      <div>操作</div>
    </div>

    <!-- 显示用户列表 -->
    <div v-for="user in users" :key="user.user_id" class="user-item">
      <div class="name-col">{{ user.nickname }}</div>
      <div>{{ user.sex === 0 ? '男' : '女' }}</div>
      <div>{{ user.email }}</div> <!-- 显示用户邮箱 -->
      <div>{{ user.register_time }}</div> <!-- 显示注册时间 -->
      <div>{{ user.record_count }}</div> <!-- 显示分析记录数 -->
      <div>
        <button class="view-btn" @click="viewUser(user.user_id)">查看</button>
        <button class="delete-btn" @click="deleteUser(user.user_id)">删除</button>
      </div>
    </div>

    <!-- 模态框显示用户详情 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-btn" @click="closeModal">&times;</span>
        <h3>用户详细信息</h3>
        <p><strong>用户名：</strong>{{ userDetails?.nickname }}</p>
        <p><strong>性别：</strong>{{ userDetails?.sex === 1 ? '男' : '女' }}</p>
        <p><strong>邮箱：</strong>{{ userDetails?.email }}</p>
        <p><strong>用户ID：</strong>{{ userDetails?.user_id }}</p>
        <p><strong>注册时间：</strong>{{ userDetails?.register_time }}</p>
        <p><strong>生日：</strong>{{ userDetails?.birth ?? '未设置' }}</p>
        <p><strong>身高：</strong>{{ userDetails?.height ?? '未设置' }}</p>
        <p><strong>体重：</strong>{{ userDetails?.weight ?? '未设置' }}</p>
        <p><strong>位置：</strong>{{ userDetails?.location ?? '未设置' }}</p>
        <p><strong>备注：</strong>{{ userDetails?.note ?? '无' }}</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button @click="changePage(page_num - 1)">上一页</button>
      <span>页码: {{ page_num }}</span>
      <button @click="changePage(page_num + 1)">下一页</button>
    </div>
  </div>
</template>



<style scoped>

/* 用户列表的样式 */
.container {
  width: 100%;
  max-width: 2100px;
  min-width: 1240px;
  padding: 20px;
}

.filter-dropdown {
  background-color: transparent;
  border: 1px solid transparent;
  color: #5a6a85;
  font-size: 15px;
  padding: 5px 10px;
  border-radius: 5px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.virtual-header {
  display: flex;
  align-items: center;
  background: #e1e9ea;
  padding: 1rem;
  font-weight: 600;
  color: #5a6a85;
}

.user-item {
  background: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #2c3e50;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-user-btn-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.add-user-btn {
  background-color: #2c3e50;
  color: white;
  font-size: 16px;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
}

.view-btn, .delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  cursor: pointer;
}

.view-btn {
  background: #007BFF;
  color: white;
}

.delete-btn {
  background: #ff5c5c;
  color: white;
}

.view-btn:hover, .delete-btn:hover {
  transform: scale(1.1);
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.5);
}

/* Modal Content */
.modal-content {
  background: linear-gradient(to right, #fff, #f7f7f7); /* Gradient background */
  margin: 10% auto;
  padding: 30px;
  border-radius: 12px; /* Rounded corners */
  width: 50%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Soft shadow for depth */
  font-family: 'Arial', sans-serif;
}

/* Modal Header */
.modal-content h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

/* Modal Paragraph */
.modal-content p {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 10px;
}

.close-btn {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close-btn:hover,
.close-btn:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
.modal-content .validity {
  font-size: 14px;
  color: #888;
  margin-top: 20px;
}



</style>
