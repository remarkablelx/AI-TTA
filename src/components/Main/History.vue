<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { get_allRecord, add_record, set_record, delete_record, search_record } from "@/api/api.ts";
import { useUserStore } from "@/stores/userStore.ts";

// 获取 Pinia store
const userStore = useUserStore();

// 示例状态和变量
const records = ref([]); // 存储获取的历史记录
const user_id = userStore.userInfo.user_id;
const page_num = ref(1); // 页码
const page_size = ref(6); // 每页条数

// 获取历史记录
const fetchRecords = async (page_num:number,page_size:number) => {
  try {
    const data = await get_allRecord(user_id, page_num, page_size);
    console.log('获取到的data是'+data)
    records.value = data.records; // 假设返回的数据中包含 records
    console.log('历史记录请求成功:', records.value);
  } catch (error) {
    console.error('历史记录请求失败:', error);
  }
};


// 新增历史记录
const addRecord = async (video_id: number) => {
  try {
    const response = await add_record(video_id, user_id); // user_id 从 Pinia store 获取
    if (response.success) {
      console.log('记录添加成功');
    } else {
      console.error('记录添加失败');
    }
  } catch (error) {
    console.error('新增历史记录失败:', error);
  }
};

// 删除分析记录
const deleteRecord = async (record_id: number) => {
  try {
    console.log('要删除的记录ID:', record_id); // 打印要删除的ID
    const response = await delete_record(record_id); // 向后端发送删除请求
    console.log(records)
    if (response.success) {
      console.log('记录删除成功');
      // 删除成功后从前端列表中移除记录
      records.value = records.value.filter(record => record.id !== record_id);
    } else {
      console.error('记录删除失败');
    }
  } catch (err) {
    console.error('删除分析记录失败:', err);
  }
};


// 筛选分析记录
const searchRecords = async (search: string, state: string, sort: number) => {
  try {
    const data = await search_record(user_id, search, state, sort, page_num.value, page_size.value);
    records.value = data.records;  // 假设返回的数据中包含 records
    console.log('筛选记录成功:', records.value);
  } catch (error) {
    console.error('筛选分析记录失败:', error);
  }
};

// 映射状态值到文本
const getStatusText = (status: number) => {
  switch (status) {
    case 0:
      return '分析中';
    case 1:
      return '已完成';
    case 2:
      return '已失效';
    default:
      return '未知状态';
  }
};

// 映射状态值到样式
const getStatusClass = (status: number) => {
  switch (status) {
    case 0:
      return 'status-processing'; // 分析中
    case 1:
      return 'status-completed'; // 已完成
    case 2:
      return 'status-expired'; // 已失效
    default:
      return '';
  }
};


// 组件加载时调用 fetchRecords
onMounted(() => {
  fetchRecords(page_num.value,page_size.value)
});


</script>

<template>
  <div class="container">
    <h2>历史记录</h2>

    <!-- 表格头部 -->
    <div class="virtual-header">
      <div class="time-col">
        <span>分析时间</span>
      </div>
      <div>视频名称</div>
      <div>
        <select class="filter-dropdown" @change="searchRecords">
          <option value="状态">状态</option>
          <option value="分析中">分析中</option>
          <option value="已完成">已完成</option>
          <option value="已失效">已失效</option>
        </select>
      </div>
      <div class="expiry-indicator">
        <span>有效期</span>
      </div>
      <div>操作</div>
    </div>

 <!-- 显示历史记录 -->
    <div v-for="record in records" :key="record.id" class="history-item">
      <div class="time-col">{{ record.time }}</div>
      <div>{{ record.video_name }}</div>
      <div>
        <span :class="['status-badge', getStatusClass(record.state)]">{{ getStatusText(record.state) }}</span>
      </div>
      <div class="expiry-indicator">
        <span>{{ record.expiration_time }}</span>
      </div>
      <div>
        <button class="check-btn" @click="updateRecord(record.id, 1, record.video_name, record.expiration_time)">修改</button>
        <button class="delete-btn" @click="deleteRecord(record.id)">删除</button>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button @click="page_num > 1 && (page_num -= 1); fetchRecords(page_num, page_size)">上一页</button>
      <span>页码: {{ page_num }}</span>
      <button @click="page_num += 1; fetchRecords(page_num, page_size)">下一页</button>
    </div>
  </div>
</template>


<style scoped>

/* 调整整体容器大小 */
.container {
  width: 100%; /* 使其宽度自适应父容器 */
  max-width: 2100px; /* 设置最大宽度，可以调整 */
  min-width: 1240px;  /* 设置最小宽度，可以调整 */
  padding: 20px; /* 调整内边距 */
  box-sizing: border-box;
}

/* 筛选框样式 */
.filter-dropdown {
  background-color: transparent; /* 透明背景 */
  border: 1px solid transparent; /* 边框颜色透明 */
  color: #5a6a85; /* 字体颜色与小标题一致 */
  font-size: 15px; /* 调整字体大小 */
  padding: 5px 10px;
  border-radius: 5px;
}

.filter-dropdown option {
  color: #5a6a85; /* 设置选项的字体颜色 */
}
.filter-dropdown {
  width: 86px; /* 设置下拉框的宽度为 200px */
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
  align-items: center; /* 保持元素垂直居中对齐 */
  background: #e1e9ea;
  border-radius: 8px 8px 0 0;
  padding: 1rem;
  font-weight: 600;
  color: #5a6a85;
}

.virtual-header > div:nth-child(1) {
  margin-right: 290px; /* 调整第一个和第二个字段之间的间距 */
}

.virtual-header > div:nth-child(2) {
  margin-right: 140px; /* 调整第二个和第三个字段之间的间距 */
}

.virtual-header > div:nth-child(3) {
  margin-right: 220px; /* 调整第三个和第四个字段之间的间距 */
}

.virtual-header > div:nth-child(4) {
  margin-right: 170px; /* 调整第四个和第五个字段之间的间距 */
}

.virtual-header > div:last-child {
  margin-right: 0; /* 移除最后一个字段的右侧间距 */
}

.history-item {
  background: white;
  gap: 1rem;
  padding: 1rem;
  display: grid;
  grid-template-columns: 2fr 1fr 1.6fr 1fr 0.8fr;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.time-col {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.status-badge {
  font-size: 0.8rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 500;
}

.status-processing {
  background: #fff6e6;
  color: #ffab00;
}

.status-completed {
  background: #e3fcef;
  color: #36b37e;
}

.status-expired {
  background: #ffeaea;
  color: #ff5c5c;
}

.expiry-indicator {
  font-size: 0.85rem;
  color: #5a6a85;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.expiring-soon {
  color: #ff5c5c;
  font-weight: 500;
}

.check-btn,
.delete-btn {
  font-size: 12px;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.check-btn {
  background: #2c3e50;
  color: white;
}

.delete-btn {
  background: #ff5c5c;
  color: white;
}

.check-btn:hover,
.delete-btn:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .history-item {
    gap: 0.2rem;
  }
  .status-badge {
    font-size: 0.8rem;
    padding: 0.1rem 0.2rem;
  }
  .check-btn,
  .delete-btn {
    font-size: 10px;
    padding: 0.4rem 0.8rem;
  }
  .time-col {
    font-size: 80%;
  }
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

.pagination button:hover {
  background-color: #34495e;
}

</style>
