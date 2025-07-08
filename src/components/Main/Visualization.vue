<template>
  <div class="table-visualization">
    <div class="chart-container">
      <div ref="trajectoryChart" class="chart"></div>
    </div>
    <div class="chart-container">
      <div ref="actionChart" class="chart"></div>
    </div>
    <div class="chart-container">
      <div ref="combinedChart" class="chart"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import type { ECharts } from 'echarts';

interface BallData {
  frame: number;
  position: { x: number; y: number } | null;
  distance: number;
}

interface ActionData {
  person_id: number;
  segment_frames: number[];
  predicted_label: string;
  confidence_score: number;
}

interface Segment {
  start_frame: number;
  end_frame: number;
}

export default defineComponent({
  name: 'TableTennisVisualization',
  props: {
    ballData: {
      type: Array as () => BallData[],
      required: true,
    },
    actionData: {
      type: Array as () => ActionData[],
      required: true,
    },
    segments: {
      type: Array as () => Segment[],
      required: true,
    },
  },
  setup(props) {
    const trajectoryChart = ref<HTMLElement | null>(null);
    const actionChart = ref<HTMLElement | null>(null);
    const combinedChart = ref<HTMLElement | null>(null);

    let trajectoryInstance: ECharts | null = null;
    let actionInstance: ECharts | null = null;
    let combinedInstance: ECharts | null = null;

    const initCharts = () => {
      if (trajectoryChart.value) {
        trajectoryInstance = echarts.init(trajectoryChart.value);
        renderTrajectoryChart();
      }

      if (actionChart.value) {
        actionInstance = echarts.init(actionChart.value);
        renderActionChart();
      }

      if (combinedChart.value) {
        combinedInstance = echarts.init(combinedChart.value);
        renderCombinedChart();
      }
    };

    const renderTrajectoryChart = () => {
      if (!trajectoryInstance) return;

      const validData = props.ballData.filter(item => item.position !== null);
      const xData = validData.map(item => (item.position as {x: number, y: number}).x);
      const yData = validData.map(item => (item.position as {x: number, y: number}).y);
      const frames = validData.map(item => item.frame);
      const distanceData = validData.map(item => item.distance);

      const option = {
        title: {
          text: '乒乓球运动轨迹',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params: any) => {
            const param = params[0];
            return `帧: ${param.data[3]}<br/>
                    X: ${param.data[0]}<br/>
                    Y: ${param.data[1]}<br/>
                    距离: ${param.data[2] === -1 ? '未知' : param.data[2]}`;
          },
        },
        xAxis: {
          name: 'X坐标',
          type: 'value',
        },
        yAxis: {
          name: 'Y坐标',
          type: 'value',
          inverse: true, // 乒乓球桌通常从上往下看
        },
        series: [
          {
            name: '球轨迹',
            type: 'line',
            data: xData.map((x, i) => [x, yData[i], distanceData[i], frames[i]]),
            symbolSize: 8,
            itemStyle: {
              color: (params: any) => {
                return params.data[2] === -1 ? '#ff0000' : '#5470C6';
              },
            },
            lineStyle: {
              color: '#5470C6',
            },
            markLine: {
              silent: true,
              data: props.segments.map(seg => ({
                xAxis: 'min',
                label: { show: false },
                lineStyle: { color: '#000', type: 'dashed' },
              })),
            },
          },
        ],
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            filterMode: 'filter',
          },
          {
            type: 'slider',
            yAxisIndex: 0,
            filterMode: 'filter',
          },
        ],
      };

      trajectoryInstance.setOption(option);
    };

    const renderActionChart = () => {
      if (!actionInstance) return;

      // 处理动作数据
      const players = Array.from(new Set(props.actionData.map(item => item.person_id))).sort();
      const frameRange = {
        min: Math.min(...props.ballData.map(item => item.frame)),
        max: Math.max(...props.ballData.map(item => item.frame)),
      };

      const series = players.map(playerId => {
        const playerActions = props.actionData.filter(item => item.person_id === playerId);
        return {
          name: `运动员 ${playerId}`,
          type: 'bar',
          stack: 'total',
          emphasis: {
            focus: 'series',
          },
          data: playerActions.map(action => ({
            value: action.confidence_score,
            itemStyle: {
              color: getActionColor(action.predicted_label),
            },
            label: action.predicted_label,
            frameStart: action.segment_frames[0],
            frameEnd: action.segment_frames[1],
          })),
        };
      });

      const option = {
        title: {
          text: '运动员动作识别',
          left: 'center',
        },
        tooltip: {
          trigger: 'item',
          formatter: (params: any) => {
            const data = params.data;
            return `运动员: ${params.seriesName}<br/>
                    动作: ${data.label}<br/>
                    置信度: ${data.value.toFixed(4)}<br/>
                    帧范围: ${data.frameStart}-${data.frameEnd}`;
          },
        },
        legend: {
          data: players.map(id => `运动员 ${id}`),
          top: 30,
        },
        xAxis: {
          type: 'category',
          data: props.actionData.map((_, i) => `动作 ${i + 1}`),
        },
        yAxis: {
          type: 'value',
          max: 1.0,
          min: 0,
        },
        series,
      };

      actionInstance.setOption(option);
    };

    const renderCombinedChart = () => {
      if (!combinedInstance) return;

      // 这里可以创建一个结合了轨迹和动作的复杂图表
      // 示例: 时间轴图表
      const option = {
        title: {
          text: '综合时间轴分析',
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#6a7985',
            },
          },
        },
        legend: {
          data: ['球位置X', '球位置Y', '球距离', '动作'],
          top: 30,
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: props.ballData.map(item => item.frame),
        },
        yAxis: [
          {
            type: 'value',
            name: '位置',
          },
          {
            type: 'value',
            name: '距离',
          },
        ],
        series: [
          {
            name: '球位置X',
            type: 'line',
            data: props.ballData.map(item => item.position?.x || null),
          },
          {
            name: '球位置Y',
            type: 'line',
            data: props.ballData.map(item => item.position?.y || null),
          },
          {
            name: '球距离',
            type: 'line',
            yAxisIndex: 1,
            data: props.ballData.map(item => item.distance === -1 ? null : item.distance),
          },
          {
            name: '动作',
            type: 'scatter',
            symbolSize: 20,
            data: props.actionData.map(action => ({
              value: [action.segment_frames[0], 0],
              label: action.predicted_label,
              confidence: action.confidence_score,
              player: action.person_id,
            })),
            itemStyle: {
              color: (params: any) => getActionColor(params.data.label),
            },
            tooltip: {
              formatter: (params: any) => {
                const data = params.data;
                return `运动员: ${data.player}<br/>
                        动作: ${data.label}<br/>
                        置信度: ${data.confidence.toFixed(4)}<br/>
                        开始帧: ${params.value[0]}`;
              },
            },
          },
        ],
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            filterMode: 'filter',
          },
        ],
      };

      combinedInstance.setOption(option);
    };

    const getActionColor = (action: string): string => {
      const colors: Record<string, string> = {
        '正手': '#91CC75',
        '反手': '#EE6666',
        '其他': '#FAC858',
      };
      return colors[action] || '#73C0DE';
    };

    const resizeCharts = () => {
      [trajectoryInstance, actionInstance, combinedInstance].forEach(instance => {
        instance?.resize();
      });
    };

    onMounted(() => {
      initCharts();
      window.addEventListener('resize', resizeCharts);
    });

    watch(() => [props.ballData, props.actionData, props.segments], () => {
      initCharts();
    }, { deep: true });

    return {
      trajectoryChart,
      actionChart,
      combinedChart,
    };
  },
});
</script>

<style scoped>
.table-visualization {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.chart-container {
  width: 100%;
  height: 400px;
  margin-bottom: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>