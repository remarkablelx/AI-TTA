<template>
  <div class="recognition-container">
    <!-- 组合图表：置信度+持续时间 -->
    <div class="chart-title"></div>
    <div ref="combinedChartRef" class="chart" style="height: 500px;"></div>

    <!-- 数据表格 -->
    <div class="chart-title">行为识别详情</div>
    <div class="data-table">
      <table>
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
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin: 15px 0 10px;
  text-align: center;
  color: #333;
}

.chart {
  width: 100%;
  min-height: 500px;
  margin-bottom: 30px;
  background: #fff;
  border-radius: 6px;
}

.data-table {
  width: 100%;
  overflow-x: auto;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #333;
}

tr:hover {
  background-color: #f5f7fa;
}

td {
  color: #666;
}
</style>