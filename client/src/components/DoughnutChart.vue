<script>
import {Line} from 'vue-chartjs'

export default {
  name: "DoughnutChart",
  extends: Line,
  props: ['data', 'value', 'year'],
  mounted() {
    this.renderLineChart();
  },
  computed: {
    chartData: function () {
      return {
        labels: this.data.years,
        datasets: [
          {
            label: 'Volume (km^3)',
            backgroundColor: '#DBF1FD',
            data: this.data.data,
            pointHoverRadius: 8,
            pointHoverBackgroundColor: '#ff5252'
          }
        ]
      };
    },
    localValue: {
      get() {
        return this.value;
      },
      set(newValue) {
        this.$emit('setValue', newValue);
      },
    },
    localYear: {
      get() {
        return this.year;
      },
      set(newYear) {
        this.$emit('setYear', newYear);
      },
    }
  },
  methods: {
    renderLineChart: function() {
      let that = this;
      this.renderChart(this.chartData, {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            gridLines: {
              display: false
            },
            ticks: {
              display: false
            }
          }]
        },
        onClick: function(evt, activeElements) {
          if(activeElements.length === 0){
            alert("Chart is clickable but you must click a data point to drill-down")
          }
          const chart = activeElements[0]._chart
          const activePoints = chart.getElementsAtEventForMode(evt, 'point', chart.options);
          const firstPoint = activePoints[0];
          that.localYear = chart.data.labels[firstPoint._index];
          let value_select = chart.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
          that.localValue = value_select;
        }
      })
    }
  },
  watch: {
    data: function() {
      // this._chart.destroy();
      this.renderLineChart();
    }
  }

}
</script>