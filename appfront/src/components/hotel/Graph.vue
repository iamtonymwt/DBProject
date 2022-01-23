<template>
<div>
  <ve-line
    :data="chartData"
    :settings="chartSettings"
    :extend="extend"
  ></ve-line>
</div>
</template>

<script>
export default {
  name: "Graph",
  data() {
    this.extend = {
      series: {
        smooth: false,
      },
    };
    this.chartSettings = {
      xAxisType: "time",
      area: true,
      smooth: false,
    };
    return {
      chartData: {
        columns: ["日期", "价格"],
        rows: [],
      },
    };
  },
};
</script>

<style scoped>
</style>