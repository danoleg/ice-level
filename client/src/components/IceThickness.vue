<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item upload" v-if="!global_is_exist">
      <md-button class="md-raised md-primary" @click="uploadData">START</md-button>
    </div>
    <div class="md-layout-item container" v-if="global_is_exist" >
      <div class="left">
        <div class="map">
          <h2 style="position: absolute">{{value}} m</h2>
          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="70vh" height="70vh" viewBox="0 0 64 64" aria-hidden="true" role="img" class="iconify iconify--emojione" preserveAspectRatio="xMidYMid meet"><circle cx="32" cy="32" r="30" fill="#3a7dce"/><path fill="#fff" d="M17.6 30.7l-.3-1.4H17l-.5.5l-.1-1.3l-.6-.5l-.4.2v.2l-.7-.3l-.5-.6l1.2-1l-2-1.6l-1-3.7l7.4 5.3l4.6-1.2l-.2-.7l.9-.2l.4-1.5l-.1-.5l.3-.4l.2-1l-.2-.4l.7-.6l-.2-1.5l1.6-.7l1.3-1.3l-.1-.7l.9.5l.8-.5l.3-.8l.4.6l4.3.2l.9.8l3.5.7l.7.7l.5-.2l.5 1.7h.3l.4-.5l3.2 1.1l.2.5l.8-.2l.9.8l.9 4.9l-.8 2.7l3.4 1l.2 2.3l-.7 1.7l1 .8l-.5 2.9l-1.7 1.3l.4 2l-1 .7l-.6-.2v1.9h-.8l.3.7l-1.7.7l.5 1l-1.1 1.2l.3.3l-.7-.2l-3.2 1.9l.2-.5l-1 .2l-.2-.5l-.8.6l-.3-.1l-.5.6l-3.6-.5l-.5-.3l-.6.3l-1.3-1l.6-.6l.9-1.8v-1.1l-.7-1.6l-.8.8l-4.7-1.2l-1 .1l-.8.5l-2.3-.2v.4l-4.8-1.7v-1h-.8l-.2-2.9l-.6.2l-.9-2.1l.2.5l-1.7-1.8h1l-.3-2l.8-1.4h.5"/></svg>
        </div>
        <div class="chart-container">
          <DoughnutChart :data="values"></DoughnutChart>
        </div>
      </div>
      <div class="right">
        <md-radio v-for="m in months" :key="m" v-model="month" v-on:change="getDataByMonth" :value="m">{{m}}</md-radio>
      </div>

    </div>
    <!--    <div class="years" v-if="global_is_exist">-->
    <!--      <md-radio v-for="y in years" :key="y" v-model="year" v-on:change="getDataByMonth" :value="y">{{y}}</md-radio>-->
    <!--    </div>-->

  </div>

</template>

<script>
import axios from "axios";
import DoughnutChart from './DoughnutChart'


export default {
  name: "IceThickness",
  components: {
    DoughnutChart
  },
  data() {
    return {
      global_is_exist: false,
      value: 0,
      values: {
        data: [],
        years: []
      },
      year: "2022",
      month: "Jan",
      processing: false,
      formdata: {},
      months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct","Nov","Dec"],
      years: ["1979",
        "1980",
        "1981",
        "1982",
        "1983",
        "1984",
        "1985",
        "1986",
        "1987",
        "1988",
        "1989",
        "1990",
        "1991",
        "1992",
        "1993",
        "1994",
        "1995",
        "1996",
        "1997",
        "1998",
        "1999",
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022"]
    };
  },
  mounted() {
    let that = this;
    this.formdata = {
      name: 'IceThickness'
    };
    axios.post('http://127.0.0.1:8011/check-global-from-iris', this.formdata).then(
        function (response) {
          if (response.data.data > 0){
            that.global_is_exist = true;

            that.formdata = {
              year: that.year,
              month: that.month
            };
            let that_i = that;
            axios.post('http://127.0.0.1:8011/data/getting/month', that.formdata).then(
                function (response) {
                  that_i.values = response.data.data;
                  that_i.value = response.data.value;
                });
          }
        });
  },
  methods: {
    uploadData() {
      this.processing = true;
      this.formdata = {};
      let that = this;
      axios.post('http://127.0.0.1:8011/import-dataset', this.formdata).then(
          function (response) {
            if(response.data.status){
              that.global_is_exist = true;

              that.formdata = {
                year: that.year,
                month: that.month
              };
              let that_i = that;
              axios.post('http://127.0.0.1:8011/data/getting/month', that.formdata).then(
                  function (response) {
                    that_i.values = response.data.data;
                    that_i.value = response.data.value;
                  });
            }
          });
    },
    getData() {
      this.formdata = {
        year: this.year,
        month: this.month
      };
      let that = this;
      axios.post('http://127.0.0.1:8011/data/getting', this.formdata).then(
          function (response) {
            that.value = response.data.data;
          });
    },
    getDataByMonth() {
      this.formdata = {
        year: this.year,
        month: this.month
      };
      let that = this;
      axios.post('http://127.0.0.1:8011/data/getting/month', this.formdata).then(
          function (response) {
            that.values = response.data.data;
            that.value = response.data.value;
          });
    },
    setData() {
      this.formdata = {
        year: this.year,
        month: this.month,
        value: this.value,
      };
      let that = this;
      axios.post('http://127.0.0.1:8011/data/set', this.formdata).then(
          function (response) {
            that.value = response.data.data;
          });
    }

  }

}
</script>

<style scoped>
.md-radio {
  display: flex;
}
.container{
  display: flex;
  height: calc(100vh - 64px);
  align-items: center;
  position: relative;
}
.left {
  width: 90%;
  height:100%;
  display: flex;
  flex-direction: column;
  align-content: space-between;
  justify-content: space-around;
}
.map{
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.right {
  width: 10%;
}
.years{
  display: flex;
  flex-wrap: wrap;
}
.chart-container{
  width: 100%;
}
.chart-container>div{
  height:100px;
  width: 100%;
}
#line-chart{
  width: 100%;
}
.upload{
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 64px);
}
</style>