<script setup lang="ts">
import { ref, computed } from 'vue';

// 示例数据，包含历史记录
const records = ref([
  { time: '2025-7-1 15:44:56', name: '视频1', status: '分析中', validity: '2025-07-08' },
  { time: '2025-5-15 19:18:29', name: '视频2', status: '已完成', validity: '2025-05-22' },
  { time: '2025-4-23 20:32:43', name: '视频3', status: '已完成', validity: '2025-04-30' },
  { time: '2025-4-23 10:34:08', name: '视频4', status: '已完成', validity: '2025-04-30' },
  { time: '2025-4-23 10:10:22', name: '视频5', status: '已完成', validity: '2025-04-30' },
  { time: '2025-4-21 22:17:12', name: '视频6', status: '已完成', validity: '2025-04-28' },
  { time: '2025-4-19 13:13:02', name: '视频7', status: '已失效', validity: '2025-04-26' },
  { time: '2025-4-19 09:33:17', name: '视频8', status: '已失效', validity: '2025-04-26' }
]);

// 筛选和排序相关的状态和变量
const searchQuery = ref('');
const selectedStatus = ref('状态');
const sortByTime = ref('asc');
const sortByValidity = ref('asc');

// 计算和过滤后的记录
const filteredAndSortedRecords = computed(() => {
  let result = records.value;

  // 搜索过滤
  if (searchQuery.value) {
    result = result.filter(item =>
      item.time.includes(searchQuery.value) ||
      item.name.includes(searchQuery.value) ||
      item.status.includes(searchQuery.value)
    );
  }

  // 状态筛选
  if (selectedStatus.value && selectedStatus.value !== '状态') {
    result = result.filter(item => item.status === selectedStatus.value);
  }

// 分析时间排序：按年、月、日、小时、分钟、秒进行排序
  if (sortByTime.value === 'asc') {
    result = result.sort((a, b) => {
      const dateA = new Date(a.time);
      const dateB = new Date(b.time);
      // 确保时间解析正确
      if (isNaN(dateA.getTime()) || isNaN(dateB.getTime())) {
        console.error("日期格式错误：", a.time, b.time);  // 打印出错的时间格式
        return 0;  // 不进行排序
      }
      return dateA.getTime() - dateB.getTime();
    });
  } else {
    result = result.sort((a, b) => {
      const dateA = new Date(a.time);
      const dateB = new Date(b.time);
      // 确保时间解析正确
      if (isNaN(dateA.getTime()) || isNaN(dateB.getTime())) {
        console.error("日期格式错误：", a.time, b.time);  // 打印出错的时间格式
        return 0;  // 不进行排序
      }
      return dateB.getTime() - dateA.getTime();
    });
  }

  // 有效期排序：按年月日时间优先级进行排序
  if (sortByValidity.value === 'asc') {
    result = result.sort((a, b) => new Date(a.validity) - new Date(b.validity));
  } else {
    result = result.sort((a, b) => new Date(b.validity) - new Date(a.validity));
  }

  return result;
});

// 切换分析时间排序
const toggleTimeSort = () => {
  sortByTime.value = sortByTime.value === 'asc' ? 'desc' : 'asc';
};

// 切换有效期排序
const toggleValiditySort = () => {
  sortByValidity.value = sortByValidity.value === 'asc' ? 'desc' : 'asc';
};
</script>

<template>
  <div class="container">
    <h2>历史记录</h2>

    <!-- 搜索框 -->
    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="搜索时间（按下方显示格式）、名称或状态"
      />
    </div>

    <!-- 表格头部 -->
    <div class="virtual-header">
      <div class="time-col" @click="toggleTimeSort">
        <span>分析时间</span>
      </div>
      <div>视频名称</div>
      <div>
        <select v-model="selectedStatus" class="filter-dropdown">
          <option value="状态">状态</option>
          <option value="分析中">分析中</option>
          <option value="已完成">已完成</option>
          <option value="已失效">已失效</option>
        </select>
      </div>
      <div class="expiry-indicator" @click="toggleValiditySort">
        <span>有效期</span>
      </div>
      <div>操作</div>
    </div>

    <!-- 显示历史记录 -->
    <div v-for="(record, index) in filteredAndSortedRecords" :key="index" class="history-item">
      <div class="time-col">{{ record.time }}</div>
      <div>{{ record.name }}</div>
      <div>
        <span class="status-badge" :class="{
          'status-processing': record.status === '分析中',
          'status-completed': record.status === '已完成',
          'status-expired': record.status === '已失效'
        }">{{ record.status }}</span>
      </div>
      <div class="expiry-indicator">
        <span :class="{'expiring-soon': new Date(record.validity) < new Date()}">
          {{ record.validity }}
        </span>
      </div>
      <div>
        <button class="check-btn">查看</button>
        <button class="delete-btn">删除</button>
      </div>
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


</style>
