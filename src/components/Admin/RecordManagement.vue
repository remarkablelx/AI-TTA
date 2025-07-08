<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { AdminGetAllRecord, AdminDeleteRecord } from "@/api/api.ts";

const records = ref<any[]>([]);
const page_num = ref(1);
const page_size = ref(10);
const isLoading = ref(false);
const isDeleting = ref<number | null>(null);
const sortOrder = ref<'asc' | 'desc'>('desc');
const searchQuery = ref(''); // 搜索关键词
const filterState = ref<number | null>(null); // 状态筛选

// 状态选项
const stateOptions = [
  { value: null, label: "全部状态" },
  { value: 0, label: "已过期" },
  { value: 1, label: "分析中" },
  { value: 2, label: "已完成" }
];

// 获取记录列表
const fetchRecords = async () => {
  isLoading.value = true;
  try {
    const response = await AdminGetAllRecord(page_num.value, page_size.value);
    if (response.code === '0') {
      let filteredRecords = response.records;

      // 应用搜索筛选
      if (searchQuery.value) {
        filteredRecords = filteredRecords.filter(record =>
          record.video_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
          record.user_id?.toString().includes(searchQuery.value)
        );
      }

      // 应用状态筛选
      if (filterState.value !== null) {
        filteredRecords = filteredRecords.filter(record => record.state === filterState.value);
      }

      // 应用排序
      filteredRecords.sort((a, b) => {
        const dateA = new Date(a.time).getTime();
        const dateB = new Date(b.time).getTime();
        return sortOrder.value === 'asc' ? dateA - dateB : dateB - dateA;
      });

      records.value = filteredRecords;
    }
  } catch (error) {
    console.error('获取记录列表失败:', error);
  } finally {
    isLoading.value = false;
  }
};

// 删除记录
const handleDelete = async (record_id: number) => {
    try {
      console.log("删除的记录是"+record_id)
      const response = await AdminDeleteRecord(record_id);
      if (response.code === '0') {
        await fetchRecords();
      }
    } catch (error) {
      console.error('删除记录失败:', error);
    } finally {
      isDeleting.value = null;
    }
};

// 切换分页
const changePage = (newPage: number) => {
  if (newPage >= 1) {
    page_num.value = newPage;
    fetchRecords();
  }
};

// 切换排序方式
const toggleSort = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  fetchRecords();
};

// 状态筛选变化
const handleStateFilterChange = (state: number | null) => {
  filterState.value = state;
  fetchRecords();
};

// 搜索
const handleSearch = () => {
  page_num.value = 1; // 搜索时重置页码
  fetchRecords();
};

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 获取状态文本
const getStateText = (state: number) => {
  switch (state) {
    case 0: return "已过期";
    case 1: return "分析中";
    case 2: return "已完成";
    default: return "未知状态";
  }
};

// 获取状态样式类
const getStateClass = (state: number) => {
  switch (state) {
    case 0: return "state-expired";
    case 1: return "state-processing";
    case 2: return "state-completed";
    default: return "";
  }
};

onMounted(() => {
  fetchRecords();
});
</script>

<template>
  <div class="record-management-container">
    <h2>记录管理</h2>

    <!-- 搜索和筛选工具栏 -->
    <div class="toolbar">
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索视频名称或用户ID"
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">搜索</button>
      </div>

      <div class="filter-section">
        <label>状态筛选：</label>
        <select v-model="filterState" @change="handleStateFilterChange(filterState)">
          <option v-for="option in stateOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <div class="table-header">
        <div class="header-item" style="width: 10%">记录ID</div>
        <div class="header-item" style="width: 10%">用户ID</div>
        <div class="header-item" style="width: 20%">视频名称</div>
        <div class="header-item" style="width: 10%">视频ID</div>
        <div class="header-item" style="width: 15%">
          <span class="sortable-header" @click="toggleSort">
            创建时间
            <span class="sort-icon">{{ sortOrder === 'asc' ? '↑' : '↓' }}</span>
          </span>
        </div>
        <div class="header-item" style="width: 15%">过期时间</div>
        <div class="header-item" style="width: 10%">状态</div>
        <div class="header-item" style="width: 10%">操作</div>
      </div>

      <div v-if="isLoading" class="loading">加载中...</div>

      <template v-else>
        <div v-if="records.length === 0" class="no-data">暂无数据</div>

        <div v-for="record in records" v-else :key="record.record_id" class="table-row">
          <div class="row-item" style="width: 10%">{{ record.record_id }}</div>
          <div class="row-item" style="width: 10%">{{ record.user_id }}</div>
          <div class="row-item" style="width: 20%">{{ record.video_name || '-' }}</div>
          <div class="row-item" style="width: 10%">{{ record.video_id }}</div>
          <div class="row-item" style="width: 15%">{{ formatDate(record.time) }}</div>
          <div class="row-item" style="width: 15%">{{ formatDate(record.expiration_time) }}</div>
          <div class="row-item" style="width: 10%">
            <span :class="getStateClass(record.state)">{{ getStateText(record.state) }}</span>
          </div>
          <div class="row-item" style="width: 5%">
            <button
              class="delete-btn"
              @click="handleDelete(record.record_id)"
            >删除</button>
          </div>
        </div>
      </template>
    </div>

    <div class="pagination">
      <button @click="changePage(page_num - 1)" :disabled="page_num === 1">上一页</button>
      <span>页码: {{ page_num }} </span>
      <button @click="changePage(page_num + 1)" :disabled="records.length < page_size">下一页</button>
    </div>
  </div>
</template>

<style scoped>
.record-management-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 20px;
  overflow: hidden;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.search-bar {
  display: flex;
  gap: 10px;
  flex: 1;
  min-width: 300px;
}

.search-bar input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.search-bar button {
  padding: 8px 16px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filter-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-section select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  min-width: 120px;
}

.table-container {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 20px;
}

.loading, .no-data {
  padding: 20px;
  text-align: center;
  color: #666;
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

.sortable-header {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.sort-icon {
  font-size: 12px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  padding: 15px 0;
  background: white;
  position: sticky;
  bottom: 0;
  border-top: 1px solid #eee;
}

.pagination button {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.delete-btn {
  padding: 4px 8px;
  background: #ff4d4f;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 12px;
  cursor: pointer;
  width: 100%;
}

.delete-btn:disabled {
  background: #ff7875;
  cursor: not-allowed;
}

/* 状态样式 */
.state-expired {
  color: #ff4d4f;
}

.state-processing {
  color: #faad14;
}

.state-completed {
  color: #52c41a;
}
</style>