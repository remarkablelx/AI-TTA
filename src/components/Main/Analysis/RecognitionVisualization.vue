<template>
  <div class="recognition-container">
    <!-- 组合图表：置信度+持续时间 -->
    <div class="chart-title"></div>
    <div ref="combinedChartRef" class="chart" style="height: 500px;"></div>

    <!-- 数据表格 -->
    <div class="chart-title">行为识别详情</div>
    <div class="data-table-container">
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>行为类型</th>
              <th>人物ID</th>
              <th>置信度</th>
              <th>起始帧</th>
              <th>结束帧</th>
              <th>持续帧数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in processedData" :key="index">
              <td>{{ item.predicted_label }}</td>
              <td>{{ item.person_id }}</td>
              <td>{{ (item.confidence_score * 100).toFixed(2) }}%</td>
              <td>{{ item.start_frame }}</td>
              <td>{{ item.end_frame }}</td>
              <td>{{ item.duration }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  recognitionData: {
    type: Array,
    required: true,
    default: () => []
  }
});

const combinedChartRef = ref<HTMLElement | null>(null);
let combinedChart: echarts.ECharts | null = null;

// 处理数据
const processedData = computed(() => {
  return props.recognitionData.map((item: any) => ({
    ...item,
    start_frame: item.segment_frames?.[0] ?? 0,
    end_frame: item.segment_frames?.[1] ?? 0,
    duration: (item.segment_frames?.[1] ?? 0) - (item.segment_frames?.[0] ?? 0) + 1
  }));
});

// 初始化组合图表
const initCombinedChart = () => {
  if (!combinedChartRef.value) {
    console.error('图表容器未找到');
    return;
  }

  try {
    // 确保容器有高度
    combinedChartRef.value.style.height = '500px';

    // 销毁旧实例
    if (combinedChart) {
      combinedChart.dispose();
    }

    combinedChart = echarts.init(combinedChartRef.value);

    // 按行为类型分组计算统计数据
    const analysisData: Record<string, {
      confidenceSum: number;
      confidenceCount: number;
      durationSum: number
    }> = {};

    processedData.value.forEach((item: any) => {
      if (!item.predicted_label) return;

      if (!analysisData[item.predicted_label]) {
        analysisData[item.predicted_label] = {
          confidenceSum: 0,
          confidenceCount: 0,
          durationSum: 0
        };
      }

      analysisData[item.predicted_label].confidenceSum += item.confidence_score || 0;
      analysisData[item.predicted_label].confidenceCount++;
      analysisData[item.predicted_label].durationSum += item.duration || 0;
    });

    const labels = Object.keys(analysisData);
    const averageConfidences = labels.map(label =>
      Number((analysisData[label].confidenceSum / analysisData[label].confidenceCount * 100).toFixed(1))
    );
    const totalDurations = labels.map(label => analysisData[label].durationSum);

    const option = {
      title: {
        text: '行为识别分析',
        left: 'center',
        textStyle: {
          fontSize: 18,
          fontWeight: 'bold',
          color: '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: (params: any) => {
          return `
            <strong>${params[0].name}</strong><br/>
            平均置信度: ${params[0].value}%<br/>
            总持续时间: ${params[1].value}帧
          `;
        }
      },
      legend: {
        data: ['平均置信度', '总持续时间'],
        top: 30
      },
      grid: {
        top: '20%',
        bottom: '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: labels,
        axisLabel: {
          rotate: 30,
          interval: 0,
          fontSize: 12
        },
        axisLine: {
          lineStyle: {
            color: '#999'
          }
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '置信度 (%)',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%',
            color: '#ee6666'
          },
          axisLine: {
            lineStyle: {
              color: '#ee6666'
            }
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        {
          type: 'value',
          name: '持续时间 (帧)',
          axisLabel: {
            color: '#5470c6'
          },
          axisLine: {
            lineStyle: {
              color: '#5470c6'
            }
          },
          splitLine: {
            show: false
          }
        }
      ],
      series: [
        {
          name: '平均置信度',
          type: 'bar',
          barWidth: '30%',
          data: averageConfidences,
          itemStyle: {
            color: '#ee6666',
            borderRadius: [4, 4, 0, 0]
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}%',
            color: '#ee6666'
          }
        },
        {
          name: '总持续时间',
          type: 'line',
          yAxisIndex: 1,
          symbolSize: 8,
          data: totalDurations,
          itemStyle: {
            color: '#5470c6'
          },
          lineStyle: {
            width: 3
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
            color: '#5470c6'
          }
        }
      ],
      animationDuration: 1000
    };

    combinedChart.setOption(option);
    console.log('组合图表初始化完成', option);
  } catch (error) {
    console.error('图表初始化失败:', error);
  }
};

// 初始化图表
const initChart = () => {
  console.log('初始化图表，数据:', props.recognitionData);
  initCombinedChart();
};

// 响应式调整
const handleResize = () => {
  combinedChart?.resize();
};

onMounted(() => {
  nextTick(() => {
    initChart();
    window.addEventListener('resize', handleResize);
  });
});

onUnmounted(() => {
  if (combinedChart) {
    combinedChart.dispose();
    combinedChart = null;
  }
  window.removeEventListener('resize', handleResize);
});

// 监听数据变化
watch(() => props.recognitionData, (newVal) => {
  console.log('recognitionData变化:', newVal);
  nextTick(() => {
    initChart();
  });
}, { deep: true });
</script>

<style scoped>
.recognition-container {
  width: 100%;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  margin: 25px 0 15px;
  text-align: center;
  color: #2c3e50;
  position: relative;
  padding-bottom: 10px;
}

.chart-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, #3498db, #2ecc71);
  border-radius: 3px;
}

.chart {
  width: 100%;
  min-height: 500px;
  margin-bottom: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.data-table-container {
  width: 100%;
  margin: 30px 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.styled-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 14px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.styled-table th {
  background: #2C3E50;
  color: white;
  font-weight: 600;
  padding: 15px 20px;
  text-align: left;
  position: sticky;
  top: 0;
}

.styled-table td {
  padding: 12px 20px;
  border-bottom: 1px solid #f0f0f0;
  color: #555;
  transition: all 0.2s ease;
}

.styled-table tr:last-child td {
  border-bottom: none;
}

.styled-table tr:hover td {
  background-color: #f8f9fa;
  transform: translateX(2px);
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #f1f5fd;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .recognition-container {
    padding: 15px;
  }

  .chart {
    height: 400px;
  }

  .styled-table th,
  .styled-table td {
    padding: 10px 12px;
    font-size: 13px;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.styled-table tbody tr {
  animation: fadeIn 0.3s ease forwards;
  opacity: 0;
}

.styled-table tbody tr:nth-child(1) { animation-delay: 0.1s; }
.styled-table tbody tr:nth-child(2) { animation-delay: 0.2s; }
.styled-table tbody tr:nth-child(3) { animation-delay: 0.3s; }
.styled-table tbody tr:nth-child(4) { animation-delay: 0.4s; }
.styled-table tbody tr:nth-child(5) { animation-delay: 0.5s; }
.styled-table tbody tr:nth-child(n+6) { animation-delay: 0.6s; }

/* 置信度颜色指示 */
.styled-table td:nth-child(3) {
  font-weight: 500;
}

.styled-table td:nth-child(3):before {
  content: '';
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 8px;
  background-color: #2ecc71;
}

.styled-table tr:hover td:nth-child(3):before {
  transform: scale(1.2);
  transition: transform 0.2s ease;
}

.styled-table td:nth-child(3)[style*="background-color:"]:before {
  background-color: inherit;
}
</style>