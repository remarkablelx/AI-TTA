<template>
  <div class="ping-pong-visualization">
    <div class="chart-container">
      <div class="chart-row">
        <!-- 球轨迹热力图 -->
        <div class="chart-item" ref="ballHeatmapChart"></div>

        <!-- 球距离变化折线图 -->
        <div class="chart-item" ref="distanceChart"></div>
      </div>

      <div class="chart-row">
        <!-- 动作分类条形图 -->
        <div class="chart-item" ref="actionChart"></div>

        <!-- 时间线分段图 -->
        <div class="chart-item" ref="timelineChart"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';

// 定义props接收数据
const props = defineProps({
  ballData: {
    type: Array as () => Array<{
      frame: number;
      position: { x: number; y: number } | null;
      distance: number;
    }>,
    required: true
  },
  actionData: {
    type: Array as () => Array<{
      person_id: number;
      segment_frames: [number, number];
      predicted_label: string;
      confidence_score: number;
    }>,
    required: true
  },
  segmentData: {
    type: Array as () => Array<{
      start_frame: number;
      end_frame: number;
    }>,
    required: true
  }
});

// 图表引用
const ballHeatmapChart = ref<HTMLElement | null>(null);
const distanceChart = ref<HTMLElement | null>(null);
const actionChart = ref<HTMLElement | null>(null);
const timelineChart = ref<HTMLElement | null>(null);

// 图表实例
let ballHeatmapInstance: echarts.ECharts;
let distanceInstance: echarts.ECharts;
let actionInstance: echarts.ECharts;
let timelineInstance: echarts.ECharts;

// 初始化图表
const initCharts = () => {
  if (ballHeatmapChart.value) {
    ballHeatmapInstance = echarts.init(ballHeatmapChart.value);
    renderBallHeatmap();
  }

  if (distanceChart.value) {
    distanceInstance = echarts.init(distanceChart.value);
    renderDistanceChart();
  }

  if (actionChart.value) {
    actionInstance = echarts.init(actionChart.value);
    renderActionChart();
  }

  if (timelineChart.value) {
    timelineInstance = echarts.init(timelineChart.value);
    renderTimelineChart();
  }
};

// 渲染球轨迹热力图
const renderBallHeatmap = () => {
  const data = props.ballData
    .filter(item => item.position !== null)
    .map(item => [item.position!.x, item.position!.y, 1]);

  const option: echarts.EChartsOption = {
    title: {
      text: '乒乓球轨迹热力图',
      left: 'center'
    },
    tooltip: {
      position: 'top'
    },
    grid: {
      height: '80%',
      top: '10%'
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: 1920, // 假设视频宽度为1920
      splitLine: { show: false }
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 1080, // 假设视频高度为1080
      splitLine: { show: false }
    },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0
    },
    series: [{
      name: '球位置',
      type: 'heatmap',
      data: data,
      pointSize: 10,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  };

  ballHeatmapInstance.setOption(option);
};

// 渲染球距离变化图
const renderDistanceChart = () => {
  const frames = props.ballData.map(item => item.frame);
  const distances = props.ballData.map(item => item.distance);

  const option: echarts.EChartsOption = {
    title: {
      text: '球距离变化',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: frames,
      name: '帧数'
    },
    yAxis: {
      type: 'value',
      name: '距离'
    },
    series: [{
      data: distances,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 3,
        color: '#5470C6'
      },
      markPoint: {
        data: [
          { type: 'max', name: '最大值' },
          { type: 'min', name: '最小值' }
        ]
      },
      markLine: {
        data: [{ type: 'average', name: '平均值' }]
      }
    }]
  };

  distanceInstance.setOption(option);
};

// 渲染动作分类图
const renderActionChart = () => {
  // 统计不同动作的数量
  const actionCounts: Record<string, number> = {};
  props.actionData.forEach(item => {
    actionCounts[item.predicted_label] = (actionCounts[item.predicted_label] || 0) + 1;
  });

  const option: echarts.EChartsOption = {
    title: {
      text: '动作分类统计',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '动作分类',
        type: 'pie',
        radius: '50%',
        data: Object.entries(actionCounts).map(([name, value]) => ({
          value,
          name
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };

  actionInstance.setOption(option);
};

// 渲染时间线分段图
const renderTimelineChart = () => {
  const data = props.segmentData.map(segment => ({
    ...segment,
    label: `片段 ${segment.start_frame}-${segment.end_frame}`
  }));

  const option: echarts.EChartsOption = {
    title: {
      text: '视频时间线分段',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c0}-{c1}帧'
    },
    xAxis: {
      type: 'value',
      name: '帧数'
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.label),
      axisLabel: {
        interval: 0,
        rotate: 30
      }
    },
    series: [
      {
        type: 'custom',
        renderItem: (params, api) => {
          const start = api.value(0) as number;
          const end = api.value(1) as number;
          const yIndex = api.value(2) as number;

          return {
            type: 'rect',
            shape: {
              x: start,
              y: yIndex * 20,
              width: end - start,
              height: 18
            },
            style: {
              fill: '#91CC75'
            }
          };
        },
        data: data.map(item => [item.start_frame, item.end_frame, data.indexOf(item)])
      }
    ]
  };

  timelineInstance.setOption(option);
};

// 响应式调整图表大小
const resizeCharts = () => {
  ballHeatmapInstance?.resize();
  distanceInstance?.resize();
  actionInstance?.resize();
  timelineInstance?.resize();
};

onMounted(() => {
  initCharts();
  window.addEventListener('resize', resizeCharts);
});

onUnmounted(() => {
  window.removeEventListener('resize', resizeCharts);
  ballHeatmapInstance?.dispose();
  distanceInstance?.dispose();
  actionInstance?.dispose();
  timelineInstance?.dispose();
});
</script>

<style scoped>
.ping-pong-visualization {
  width: 100%;
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}

.chart-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chart-row {
  display: flex;
  gap: 20px;
  height: 400px;
}

.chart-item {
  flex: 1;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

@media (max-width: 1200px) {
  .chart-row {
    flex-direction: column;
    height: auto;
  }

  .chart-item {
    height: 350px;
  }
}
</style>