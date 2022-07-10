<script>
import {Line} from 'vue-chartjs'

export default {
  name: "DoughnutChart",
  extends: Line,
  props: ['data', 'options'],
  mounted() {
    this.renderLineChart();
  },
  computed: {
    chartData: function () {
      return {
        labels: this.data.years,
        datasets: [
          {
            label: 'Thickness (m)',
            backgroundColor: '#DBF1FD',
            data: this.data.data
          }
        ]
      };
    }
  },
  methods: {
    renderLineChart: function() {
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