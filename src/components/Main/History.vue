<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { get_allRecord, add_record, get_record, delete_record, search_record } from "@/api/api.ts";
import { useUserStore } from "@/stores/userStore.ts";
import { useVideoStore } from "@/stores/videoStore.ts"
// 获取 Pinia store
const userStore = useUserStore();
const videoStore = useVideoStore();

// 示例状态和变量
const records = ref([]); // 存储获取的历史记录
const user_id = userStore.userInfo.user_id;
const page_num = ref(1); // 页码
const page_size = ref(6); // 每页条数
const video_id = videoStore.videoInfo.video_id;


// 控制显示记录详情的模态框
const showModal = ref(false); // 控制模态框的显示
const recordDetails = ref<any>(null); // 存储获取到的记录详情
// 筛选量
const searchQuery = ref(""); // 搜索框内容
const selectedState = ref(""); // 默认状态为“分析中” (0: "分析中", 1: "已完成", 2: "已失效")
const sortBy = ref<'time' | null>('time'); // 当前排序的列，默认按“分析时间”排序
const sortOrder = ref(1); // 排序方式（1：升序，-1：降序），默认升序

// 默认搜索框的值
const defaultSearchValue = ""; // 默认值为空，表示所有记录
// 获取历史记录
const fetchRecords = async (page_num:number,page_size:number) => {
  try {
    const data = await get_allRecord(user_id, page_num, page_size);
    console.log('获取到的data是'+data.records)
    records.value = data.records; // 假设返回的数据中包含 records
    console.log('历史记录请求成功:', records.value);
  } catch (error) {
    console.error('历史记录请求失败:', error);
  }
};


// 新增历史记录
const addRecord = async () => {
  try {
    const response = await add_record(video_id, user_id); // user_id 从 Pinia store 获取
    console.log(video_id);
    if (response.code === "0") {
      console.log('记录添加成功');
      fetchRecords(page_num.value, page_size.value);
    } else {
      console.error('记录添加失败');
    }
  } catch (error) {
    console.error('新增历史记录失败:', error);
  }
};

// 删除分析记录
const deleteRecord = async (record_id: number) => {
  console.log(record_id);
  try {
    console.log('要删除的记录ID:', record_id); // 打印要删除的ID
    const response = await delete_record(record_id); // 向后端发送删除请求
    console.log(response);
    if (response.code === "0") {
      console.log('记录删除成功');
      fetchRecords(page_num.value, page_size.value);
    } else {
      console.error('记录删除失败');
    }
  } catch (err) {
    console.error('删除分析记录失败:', err);
  }
};


// 查看记录的函数
const viewRecord = async (record_id: number) => {
  try {
    const data = await get_record(record_id);
    recordDetails.value = data.record; // 将返回的记录信息存储到`recordDetails`
    showModal.value = true; // 显示模态框
  } catch (error) {
    console.error('查看记录失败:', error);
  }
};

// 关闭模态框
const closeModal = () => {
  showModal.value = false;
};


// 筛选分析记录
const searchRecords = async () => {
  try {

    const state = selectedState.value === "" ? null : selectedState.value;
    const sort = sortOrder.value === 1 ? 'time_asc' : 'time_desc';

    const data = await search_record(user_id, searchQuery.value || defaultSearchValue, state, sort, page_num.value, page_size.value);
    console.log("获得的data"+data)
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

// 切换排序（分析时间）
const toggleSort = () => {
  // 切换排序状态（升序、降序）
  sortOrder.value = sortOrder.value === 1 ? -1 : 1;
  searchRecords(); // 更新记录
};


// 切换分页时保持当前筛选条件
const changePage = (newPageNum: number) => {
  if (newPageNum >= 1) {
    page_num.value = newPageNum; // 更新当前页码
    searchRecords(); // 使用当前页码以及筛选条件重新获取数据
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
    <div>
      <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索内容"
          @input="searchRecords"
      />
    </div>
    <!-- 新增历史记录按钮 -->
    <div class="add-record-btn-container">
      <button @click="addRecord" class="add-record-btn">新增历史记录</button>
    </div>

    <!-- 表格头部 -->
    <div class="virtual-header">
      <div class="time-col" @click="toggleSort()">
        <span>分析时间</span>
        <span>{{ sortBy === 'time' ? (sortOrder === 1 ? '↑' : '↓') : '' }}</span>
      </div>
      <div>视频名称</div>
      <div>
        <select class="filter-dropdown" v-model="selectedState" @change="searchRecords">
          <option value=''>状态</option>
          <option value=0>分析中</option>
          <option value=1>已完成</option>
          <option value=2>已失效</option>
        </select>
      </div>
      <div class="expiry-indicator">
        <span>有效期</span>
      </div>
      <div>操作</div>
    </div>

 <!-- 显示历史记录 -->
    <div v-for="record in records" :key="record.record_id" class="history-item">
      <div class="time-col">{{ record.time }}</div>
      <div>{{ record.video_name }}</div>
      <div>
        <span :class="['status-badge', getStatusClass(record.state)]">{{ getStatusText(record.state) }}</span>
      </div>
      <div class="expiry-indicator">
        <span>{{ record.expiration_time }}</span>
      </div>
      <div>
        <button class="view-btn" @click="viewRecord(record.record_id)">查看</button>
        <button class="update-btn" @click="updateRecord(record.record_id, 1, record.video_name, record.expiration_time)">修改</button>
        <button class="delete-btn" @click="deleteRecord(record.record_id)">删除</button>
      </div>
    </div>

      <!-- 模态框显示记录详情 -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close-btn" @click="closeModal">&times;</span>
        <h3>分析记录详情</h3>
        <p><strong>分析记录编号：</strong>{{ recordDetails?.record_id }}</p>
        <p><strong>分析时间：</strong>{{ recordDetails?.time }}</p>
        <p><strong>视频名称：</strong>{{ recordDetails?.video_name }}</p>
        <p><strong>状态：</strong>{{ getStatusText(recordDetails?.state) }}</p>
        <p><strong>有效期：</strong>{{ recordDetails?.expiration_time }}</p>
        <p><strong>用户ID：</strong>{{ recordDetails?.user_id }}</p>
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
  margin-right: 100px; /* 调整第三个和第四个字段之间的间距 */
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

.update-btn,
.delete-btn,
.view-btn {
  font-size: 12px;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-btn {
  background: #2c3e50;
  color: white;
}

.delete-btn {
  background: #ff5c5c;
  color: white;
}
.view-btn{
  background: #007BFF;
  color: white;
}

.update-btn:hover,
.delete-btn:hover,
.view-btn:hover {
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
  .update-btn,
  .delete-btn,
  .view-btn{
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


/* Container for the button */
.add-record-btn-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end; /* Align the button to the right */
}

/* Button Styling */
.add-record-btn {
  background-color: #2c3e50; /* Green background */
  color: white; /* White text */
  font-size: 16px;
  font-weight: bold;
  padding: 12px 24px; /* Adequate padding for the button */
  border: none;
  border-radius: 5px; /* Rounded corners */
  cursor: pointer;
  transition: all 0.3s ease-in-out; /* Smooth hover transition */
}

/* Hover Effect */
.add-record-btn:hover {
  background-color: #45a049; /* Darker green on hover */
  transform: scale(1.05); /* Slightly increase button size */
}

/* Focus Effect */
.add-record-btn:focus {
  outline: none; /* Remove the default focus outline */
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3); /* Add a soft shadow on focus */
}

/* Active Effect */
.add-record-btn:active {
  background-color: #3e8e41; /* Even darker green when clicked */
  transform: scale(0.98); /* Slightly reduce button size */
}

/* Modal Background */
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
