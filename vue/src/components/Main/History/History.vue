<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { get_allRecord, add_record, get_record, delete_record, search_record, generate_result } from "@/api/api.ts";
import { useUserStore } from "@/stores/userStore.ts";
import { useVideoStore } from "@/stores/videoStore.ts"
import Video from "@/components/Main/Analysis/Video.vue";

interface RecordItem {
  record_id: number;
  time: string;
  video_name: string;
  state: number;
  expiration_time: string;
  result_id: number;
  user_id: number;
  video_id: number;
}

// 获取 Pinia store
const userStore = useUserStore();
const videoStore = useVideoStore();

// 定义事件
const emit = defineEmits(['toggle-view']);

// 示例状态和变量
const records = ref<RecordItem[]>([]);
const user_id = userStore.userInfo.user_id;
const page_num = ref(1); // 页码
const page_size = ref(6); // 每页条数
const video_id = videoStore.videoInfo.video_id;
const result_id = ref<number>(0); // 确保 result_id 初始化为有效的数字，默认为 0

// 控制显示记录详情的模态框
const showModal = ref(false);
const recordDetails = ref<RecordItem | null>(null);


// 筛选量
const searchQuery = ref(""); // 搜索框内容
const selectedState = ref(""); // 默认状态为"分析中" (0: "分析中", 1: "已完成", 2: "已失效")
const sortBy = ref<'time' | null>('time'); // 当前排序的列，默认按"分析时间"排序
const sortOrder = ref(1); // 排序方式（1：升序，-1：降序），默认升序

// 默认搜索框的值
const defaultSearchValue = ""; // 默认值为空，表示所有记录


// 新增时间格式化函数
const formatDate = (dateString: string) => {
  if (!dateString) return '';

  try {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false
    }).replace(/\//g, '-');
  } catch (e) {
    return dateString; // 如果解析失败，返回原始字符串
  }
};

// 获取历史记录
const fetchRecords = async (page_num: number, page_size: number) => {
  try {
    const data = await get_allRecord(user_id, page_num, page_size);
    console.log('获取到的data是' + data.records);
    records.value = data.records; // 假设返回的数据中包含 records
    console.log('历史记录请求成功:', records.value);
  } catch (error) {
    console.error('历史记录请求失败:', error);
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
      await fetchRecords(page_num.value, page_size.value);
    } else {
      console.error('记录删除失败');
    }
  } catch (err) {
    console.error('删除分析记录失败:', err);
  }
};

const viewRecord = async (record_id: number) => {
  try {
    console.log("现在的record_id是" + record_id);
    const response = await get_record(record_id);
    const record = response.record; // 这是从响应中提取的 record 对象
    console.log(record)
    if (record) {
      // 更新 recordDetails
      recordDetails.value = {
        expiration_time: record.expiration_time,
        record_id: record.record_id,
        result_id: record.result_id,
        state: record.state,
        time: record.time,
        user_id: record.user_id,
        video_id: record.video_id,
        video_name: record.video_name
      };
      console.log("现在的recordDetails是", recordDetails.value);
      result_id.value = recordDetails.value.record_id;
      console.log("现在的result_id是" + result_id);

      // 发送事件给父组件，切换到分析界面
      emit('toggle-view', 'analysis', record.result_id);
    } else {
      console.error('没有找到记录');
    }
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
    const state = selectedState.value === "" ? -1 : parseInt(selectedState.value, 10);
    const sort = sortOrder.value === 1 ? 'time_asc' : 'time_desc';

    const data = await search_record(user_id, searchQuery.value || defaultSearchValue, state, sort, page_num.value, page_size.value);
    console.log("获得的data" + data);
    records.value = data.records;  // 假设返回的数据中包含 records
    console.log('筛选记录成功:', records.value);
  } catch (error) {
    console.error('筛选分析记录失败:', error);
  }
};

// 进行分析函数
const analyzeRecord = async (record_id: number) => {
  try {
    console.log("record_id是" + record_id);
    alert("记录"+record_id+"正在分析中")
    const analysisResult = await generate_result(record_id); // 调用生成分析结果的API
    result_id.value = analysisResult.result.result_id; // 存储结果 ID
    console.log('分析结果存储成功:', analysisResult);
    alert("记录"+record_id+"分析完成")
  } catch (error) {
    console.error('分析失败:', error);
  }
};

// 映射状态值到文本
const getStatusText = (status: number) => {
  switch (status) {
    case 0: return '分析中';
    case 1: return '分析中';
    case 2: return '已完成';
    default: return '未知状态';
  }
};

// 映射状态值到样式
const getStatusClass = (status: number) => {
  switch (status) {
    case 0: return 'status-processing'; // 分析中
    case 1: return 'status-expired'; // 已完成
    case 2: return 'status-completed'; // 已失效
    default: return '';
  }
};

// 切换排序（分析时间）
const toggleSort = () => {
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
  fetchRecords(page_num.value, page_size.value);
});
</script>

<template>
  <div class="container">
    <h2>历史记录</h2>
    <div class="search-container">
      <input
          v-model="searchQuery"
          type="text"
          placeholder="输入视频名称搜索"
          class="search-input"
          @keyup.enter="searchRecords"
      />
      <button class="search-btn" @click="searchRecords">
        <span>搜索</span>
      </button>
    </div>

    <!-- 使用 v-if="false" 隐藏子组件，仍然传递 result_id -->
    <Video :result_id="result_id" v-if="false" />

    <!-- 表格头部 -->
    <div class="virtual-header">
      <div class="time-col" @click="toggleSort()">
        <span>分析时间</span>
        <span>{{ sortBy === 'time' ? (sortOrder === 1 ? '↑' : '↓') : '' }}</span>
      </div>
      <div>视频名称</div>
      <div>
        <select class="filter-dropdown" v-model="selectedState" @change="searchRecords">
          <option value=''>已失效</option>
          <option value=0>分析中</option>
          <option value=1>分析中</option>
          <option value=2>已完成</option>
        </select>
      </div>
      <div class="expiry-indicator">
        <span>有效期</span>
      </div>
      <div>操作</div>
    </div>

  <!-- 显示历史记录 -->
  <div v-for="record in records" :key="record.record_id" class="history-item">
    <div class="time-col">{{ formatDate(record.time) }}</div>
    <div>{{ record.video_name }}</div>
    <div>
      <span :class="['status-badge', getStatusClass(record.state)]">{{ getStatusText(record.state) }}</span>
    </div>
    <div class="expiry-indicator">
      <span>{{ formatDate(record.expiration_time) }}</span>
    </div>
    <div>
      <button class="analyze-btn" @click="analyzeRecord(record.record_id)">分析</button>
      <button class="view-btn" @click="viewRecord(record.record_id)">查看</button>
      <button class="delete-btn" @click="deleteRecord(record.record_id)">删除</button>
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
/* 整体容器样式 */
.container {
  width: 100%;
  max-width: 2100px;
  min-width: 1240px;
  padding: 20px;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif;
}

/* 标题样式 */
h2 {
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 24px;
}

/* 搜索框样式 */
input[type="text"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

/* 表格头部样式 - 修改为固定列宽 */
.virtual-header {
  display: grid;
  grid-template-columns: 300px 200px 150px 300px 200px;
  background: #e1e9ea;
  border-radius: 8px 8px 0 0;
  padding: 1rem;
  font-weight: 600;
  color: #5a6a85;
  margin-bottom: 5px;
}

.virtual-header > div {
  padding: 0 10px;
}

/* 时间列特殊处理 */
.virtual-header .time-col {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

/* 历史记录项样式 - 与头部相同的列宽 */
.history-item {
  display: grid;
  grid-template-columns: 300px 200px 150px 300px 200px;
  align-items: center;
  background: white;
  padding: 1rem;
  margin-bottom: 5px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.history-item > div {
  padding: 0 10px;
}

/* 操作按钮容器 */
.history-item > div:last-child {
  display: flex;
  gap: 5px;
}

/* 状态标签样式 */
.status-badge {
  display: inline-block;
  font-size: 0.8rem;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 500;
  text-align: center;
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

/* 按钮样式 */
button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
}

.analyze-btn {
  background: #2c3e50;
  color: white;
}

.view-btn {
  background: #007BFF;
  color: white;
}

.delete-btn {
  background: #ff5c5c;
  color: white;
}

button:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.pagination button {
  background-color: #2c3e50;
  color: white;
  padding: 8px 16px;
}

.pagination button:hover {
  background-color: #34495e;
}

.pagination span {
  color: #5a6a85;
}

/* 筛选下拉框样式 */
.filter-dropdown {
  background-color: transparent;
  border: 1px solid transparent;
  color: #5a6a85;
  font-size: 15px;
  padding: 5px 5px;
  border-radius: 5px;
  width: 100%;
  cursor: pointer;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .container {
    min-width: 100%;
    padding: 10px;
  }

  .virtual-header,
  .history-item {
    grid-template-columns: 200px 150px 80px 150px 120px;
    font-size: 14px;
  }

  button {
    padding: 0.4rem 0.8rem;
    font-size: 11px;
  }
}

@media (max-width: 768px) {
  .virtual-header,
  .history-item {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .virtual-header > div,
  .history-item > div {
    width: 100%;
    text-align: left;
  }

  .history-item > div:last-child {
    justify-content: flex-start;
  }
}

.search-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  width: 100%;
  max-width: 400px;
  align-items: stretch; /* 确保子元素高度一致 */
}

.search-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  min-width: 200px;
  transition: border-color 0.3s;
  height: 40px; /* 固定高度 */
  box-sizing: border-box; /* 包含padding */
  line-height: 20px; /* 确保文本垂直居中 */
}

.search-btn {
  padding: 0 20px; /* 调整垂直padding为0 */
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  height: 40px; /* 与输入框相同高度 */
  box-sizing: border-box; /* 包含padding */
  line-height: 40px; /* 确保文本垂直居中 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

</style>