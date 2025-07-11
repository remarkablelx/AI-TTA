<template>
  <div class="visualization-container">
    <!-- 第一张图：XY坐标散点图（所有帧） -->
    <div ref="allFramesChartRef" class="chart"></div>

    <!-- 第二张图：XY坐标散点图（当前帧） -->
    <div ref="currentFrameChartRef" class="chart"></div>

    <div class="frame-control">
      <div class="slider-container">
        <input
          type="range"
          v-model.number="currentFrame"
          :min="minFrame"
          :max="maxFrame"
          step="1"
          @input="handleSliderChange"
          class="slider"
        >
      </div>

      <div class="controls">
        <button @click="prevFrame" class="control-btn" title="上一帧">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/>
          </svg>
        </button>

        <button @click="togglePlay" class="play-btn" :title="isPlaying ? '暂停' : '播放'">
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path v-if="!isPlaying" d="M8 5v14l11-7z"/>
            <path v-else d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
        </button>

        <button @click="nextFrame" class="control-btn" title="下一帧">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </button>

        <span class="frame-info">帧: {{ currentFrame }}</span>

        <div class="speed-control">
          <label>速度:</label>
          <select v-model="playSpeed" @change="adjustPlaySpeed">
            <option value="250">慢速</option>
            <option value="150">正常</option>
            <option value="80">快速</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import * as echarts from 'echarts';

interface BallDataItem {
  frame: number;
  position: { x: number; y: number; } | null;
}

const props = defineProps({
  ballData: {
    type: Array as () => BallDataItem[],
    required: true,
    default: () => []
  }
});

const allFramesChartRef = ref<HTMLElement | null>(null);
const currentFrameChartRef = ref<HTMLElement | null>(null);
const currentFrame = ref(0);
const isPlaying = ref(false);
const playInterval = ref<number | null>(null);
const playSpeed = ref('150'); // 默认正常速度
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

const framesWithPosition = computed(() => {
  return props.ballData
    .filter((item: BallDataItem) => item.position !== null)
    .map((item) => item.frame);
});

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

    const validData = props.ballData.filter((item: BallDataItem) => item.position !== null);
    const xValues = validData.map(item => item.position!.x);
    const yValues = validData.map(item => item.position!.y);
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

    allFramesChart.on('click', (params: any) => {
      if (params.data) {
        stopPlayback();
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
  stopPlayback();
  const currentIndex = framesWithPosition.value.indexOf(currentFrame.value);
  if (currentIndex > 0) {
    currentFrame.value = framesWithPosition.value[currentIndex - 1];
  } else if (currentFrame.value > minFrame.value) {
    currentFrame.value--;
  }
};

const nextFrame = () => {
  stopPlayback();
  const currentIndex = framesWithPosition.value.indexOf(currentFrame.value);
  if (currentIndex < framesWithPosition.value.length - 1) {
    currentFrame.value = framesWithPosition.value[currentIndex + 1];
  } else if (currentFrame.value < maxFrame.value) {
    currentFrame.value++;
  }
};

// 滑块处理
const handleSliderChange = () => {
  stopPlayback();
  updateCurrentFrameChart();
};

// 播放控制
const togglePlay = () => {
  if (isPlaying.value) {
    stopPlayback();
  } else {
    startPlayback();
  }
};

const startPlayback = () => {
  if (playInterval.value) clearInterval(playInterval.value);

  isPlaying.value = true;

  // 如果当前是最后一帧，从头开始播放
  if (currentFrame.value >= maxFrame.value) {
    currentFrame.value = minFrame.value;
  }

  playInterval.value = setInterval(() => {
    if (currentFrame.value >= maxFrame.value) {
      stopPlayback();
      return;
    }
    currentFrame.value++;
  }, parseInt(playSpeed.value));
};

const stopPlayback = () => {
  if (playInterval.value) {
    clearInterval(playInterval.value);
    playInterval.value = null;
  }
  isPlaying.value = false;
};

const adjustPlaySpeed = () => {
  if (isPlaying.value) {
    stopPlayback();
    startPlayback();
  }
};

// 初始化所有图表
const initCharts = () => {
  if (!props.ballData.length) return;

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
  stopPlayback();
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

.chart {
  width: 100%;
  height: 350px;
  margin-bottom: 20px;
  background: #fff;
  border-radius: 6px;
}

.frame-control {
  margin-top: 15px;
}

.slider-container {
  margin-bottom: 15px;
}

.slider {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  background: #e0e0e0;
  border-radius: 4px;
  outline: none;
  transition: all 0.2s;
}

.slider:hover {
  height: 10px;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  background: #5470C6;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  background: #3a56b4;
}

.controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.control-btn, .play-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #5470C6;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
}

.control-btn:hover, .play-btn:hover {
  background: #3a56b4;
  transform: scale(1.05);
}

.control-btn:active, .play-btn:active {
  transform: scale(0.95);
}

.play-btn {
  width: 50px;
  height: 50px;
  background: #EE6666;
}

.play-btn:hover {
  background: #d84c4c;
}

.frame-info {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  min-width: 80px;
  text-align: center;
}

.speed-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.speed-control label {
  font-size: 14px;
  color: #666;
}

.speed-control select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  outline: none;
}

.speed-control select:focus {
  border-color: #5470C6;
}
</style>