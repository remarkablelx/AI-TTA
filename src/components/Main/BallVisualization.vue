<template>
  <div class="visualization-container">
    <!-- 第一张图：XY坐标散点图（所有帧） -->
    <div class="chart-title"></div>
    <div ref="allFramesChartRef" class="chart"></div>

    <!-- 第二张图：XY坐标散点图（当前帧） -->
    <div class="chart-title"></div>
    <div ref="currentFrameChartRef" class="chart"></div>

    <div class="frame-control">
      <input
        type="range"
        v-model.number="currentFrame"
        :min="minFrame"
        :max="maxFrame"
        step="1"
        @input="handleSliderChange"
        class="slider"
      >
      <div class="frame-info">
        <span>当前帧: {{ currentFrame }}</span>
        <button @click="prevFrame" class="nav-btn">←</button>
        <button @click="nextFrame" class="nav-btn">→</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  ballData: {
    type: Array,
    required: true,
    default: () => []
  }
});

const allFramesChartRef = ref<HTMLElement | null>(null);
const currentFrameChartRef = ref<HTMLElement | null>(null);
const currentFrame = ref(0);
let allFramesChart: echarts.ECharts | null = null;
let currentFrameChart: echarts.ECharts | null = null;

// 计算属性
const minFrame = computed(() => {
  return props.ballData.length > 0 ? props.ballData[0].frame : 0;
});

const maxFrame = computed(() => {
  return props.ballData.length > 0
    ? props.ballData[props.ballData.length - 1].frame
    : 0;
});

// 获取所有有位置数据的帧
const framesWithPosition = computed(() => {
  return props.ballData
    .filter((item: any) => item.position !== null)
    .map((item: any) => item.frame);
});

// 获取当前帧数据
const currentFrameData = computed(() => {
  return props.ballData.find((item: any) => item.frame === currentFrame.value);
});

// 初始化所有帧散点图
const initAllFramesChart = () => {
  if (!allFramesChartRef.value) return;

  try {
    allFramesChartRef.value.style.height = '350px';
    if (allFramesChart) allFramesChart.dispose();

    allFramesChart = echarts.init(allFramesChartRef.value);

    // 过滤出有位置数据的点
    const validData = props.ballData.filter((item: any) => item.position !== null);

    // 计算坐标范围
    const xValues = validData.map(item => item.position.x);
    const yValues = validData.map(item => item.position.y);
    const xExtent = [Math.min(...xValues), Math.max(...xValues)];
    const yExtent = [Math.min(...yValues), Math.max(...yValues)];

    const option = {
      title: {
        text: '乒乓球运动轨迹（所有帧）',
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const data = params.data;
          return `帧: ${data.frame}<br/>X: ${data.value[0].toFixed(1)}<br/>Y: ${data.value[1].toFixed(1)}`;
        }
      },
      grid: {
        top: '15%',
        right: '5%',
        bottom: '15%',
        left: '10%'
      },
      xAxis: {
        name: 'X坐标',
        nameLocation: 'middle',
        nameGap: 30,
        type: 'value',
        min: xExtent[0] - 50,
        max: xExtent[1] + 50,
        axisLine: {
          lineStyle: {
            color: '#666'
          }
        },
        splitLine: {
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      yAxis: {
        name: 'Y坐标',
        nameLocation: 'middle',
        nameGap: 30,
        type: 'value',
        min: yExtent[0] - 50,
        max: yExtent[1] + 50,
        axisLine: {
          lineStyle: {
            color: '#666'
          }
        },
        splitLine: {
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      series: [{
        name: '位置',
        type: 'scatter',
        symbolSize: (data: any) => {
          return data.frame === currentFrame.value ? 16 : 8;
        },
        data: validData.map((item: any) => ({
          value: [item.position.x, item.position.y],
          frame: item.frame
        })),
        itemStyle: {
          color: (params: any) => {
            return params.data.frame === currentFrame.value ? '#EE6666' : '#5470C6';
          }
        },
        emphasis: {
          itemStyle: {
            color: '#EE6666'
          }
        }
      }],
      animationDuration: 500
    };

    allFramesChart.setOption(option);

    // 添加点击事件
    allFramesChart.on('click', (params: any) => {
      if (params.data) {
        currentFrame.value = params.data.frame;
      }
    });

    window.addEventListener('resize', () => {
      allFramesChart?.resize();
    });
  } catch (error) {
    console.error('所有帧散点图初始化失败:', error);
  }
};

// 初始化当前帧散点图
const initCurrentFrameChart = () => {
  if (!currentFrameChartRef.value) return;

  try {
    currentFrameChartRef.value.style.height = '350px';
    if (currentFrameChart) currentFrameChart.dispose();

    currentFrameChart = echarts.init(currentFrameChartRef.value);
    updateCurrentFrameChart();

    window.addEventListener('resize', () => {
      currentFrameChart?.resize();
    });
  } catch (error) {
    console.error('当前帧散点图初始化失败:', error);
  }
};

// 更新当前帧图表
const updateCurrentFrameChart = () => {
  if (!currentFrameChart) return;

  const pointData = currentFrameData.value?.position
    ? [{
        value: [currentFrameData.value.position.x, currentFrameData.value.position.y],
        frame: currentFrame.value
      }]
    : [];

  const option = {
    title: {
      text: `乒乓球位置（帧: ${currentFrame.value}${pointData.length ? '' : ' (无数据)'}）`,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const data = params.data;
        return `帧: ${data.frame}<br/>X: ${data.value[0].toFixed(1)}<br/>Y: ${data.value[1].toFixed(1)}`;
      }
    },
    grid: {
      top: '15%',
      right: '5%',
      bottom: '15%',
      left: '10%'
    },
    xAxis: {
      name: 'X坐标',
      nameLocation: 'middle',
      nameGap: 30,
      type: 'value',
      min: 0,
      max: 1000,
      axisLine: {
        lineStyle: {
          color: '#666'
        }
      },
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    yAxis: {
      name: 'Y坐标',
      nameLocation: 'middle',
      nameGap: 30,
      type: 'value',
      min: 0,
      max: 1000,
      axisLine: {
        lineStyle: {
          color: '#666'
        }
      },
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      name: '位置',
      type: 'scatter',
      symbolSize: 24,
      data: pointData,
      itemStyle: {
        color: '#EE6666',
        shadowBlur: 10,
        shadowColor: 'rgba(0, 0, 0, 0.3)'
      },
      label: {
        show: pointData.length > 0,
        formatter: (params: any) => {
          return `X:${params.value[0].toFixed(1)}\nY:${params.value[1].toFixed(1)}`;
        },
        position: 'top',
        fontSize: 12,
        backgroundColor: 'rgba(255,255,255,0.8)',
        padding: [4, 8],
        borderRadius: 4,
        distance: 10
      }
    }],
    animationDuration: 300
  };

  currentFrameChart.setOption(option);

  // 更新所有帧图表中的当前帧高亮
  if (allFramesChart) {
    allFramesChart.setOption({
      series: [{
        symbolSize: (data: any) => {
          return data.frame === currentFrame.value ? 16 : 8;
        },
        itemStyle: {
          color: (params: any) => {
            return params.data.frame === currentFrame.value ? '#EE6666' : '#5470C6';
          }
        }
      }]
    });
  }
};

// 帧导航
const prevFrame = () => {
  // 找到前一个有数据的帧
  const currentIndex = framesWithPosition.value.indexOf(currentFrame.value);
  if (currentIndex > 0) {
    currentFrame.value = framesWithPosition.value[currentIndex - 1];
  } else if (currentFrame.value > minFrame.value) {
    currentFrame.value--;
  }
};

const nextFrame = () => {
  // 找到后一个有数据的帧
  const currentIndex = framesWithPosition.value.indexOf(currentFrame.value);
  if (currentIndex < framesWithPosition.value.length - 1) {
    currentFrame.value = framesWithPosition.value[currentIndex + 1];
  } else if (currentFrame.value < maxFrame.value) {
    currentFrame.value++;
  }
};

// 滑块处理
const handleSliderChange = () => {
  updateCurrentFrameChart();
};

// 初始化所有图表
const initCharts = () => {
  if (!props.ballData.length) return;

  // 设置初始帧为第一个有数据的帧
  const firstValidFrame = framesWithPosition.value[0] || minFrame.value;
  currentFrame.value = firstValidFrame;

  initAllFramesChart();
  initCurrentFrameChart();
};

// 监听数据变化
watch(() => props.ballData, (newVal) => {
  if (newVal?.length) {
    nextTick(initCharts);
  }
}, { deep: true });

// 监听当前帧变化
watch(() => currentFrame.value, () => {
  updateCurrentFrameChart();
});

onMounted(() => {
  if (props.ballData.length) {
    nextTick(initCharts);
  }
});

onUnmounted(() => {
  [allFramesChart, currentFrameChart].forEach(chart => {
    if (chart) {
      chart.dispose();
      chart = null;
    }
  });

  window.removeEventListener('resize', () => {
    allFramesChart?.resize();
    currentFrameChart?.resize();
  });
});
</script>

<style scoped>
.visualization-container {
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
  height: 350px;
  margin-bottom: 30px;
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.frame-control {
  margin-top: 20px;
  padding: 0 20px;
}

.slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  background: #e0e0e0;
  border-radius: 4px;
  outline: none;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  background: #5470C6;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.frame-info {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 12px;
  font-size: 14px;
  color: #666;
}

.frame-info span {
  margin: 0 15px;
  font-weight: bold;
  color: #333;
}

.nav-btn {
  padding: 4px 12px;
  background: #5470C6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: #3a56b4;
}

.nav-btn:active {
  transform: scale(0.98);
}
</style>