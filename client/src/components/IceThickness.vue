<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item upload" v-if="!global_is_exist && checked">
      <md-button class="md-raised md-primary" @click="uploadData">START</md-button>
    </div>
    <div class="md-layout-item container" v-if="global_is_exist" >
      <md-button class="md-fab" @click="active = true" style="position:absolute; top: 0px; left: 15px">
        <md-icon>edit</md-icon>
      </md-button>
      <div>
        <md-dialog-prompt
            :md-active.sync="active"
            v-model="value"
            :md-title= this.getMessage()
            md-input-placeholder="100"
            type="number"
            v-on:md-confirm="setData"
            md-confirm-text="Done" />
      </div>
      <div class="left">
        <div class="map">
          <h2 style="position: absolute">{{value}} km&sup3;</h2>
          <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="70vh" height="70vh" viewBox="0 0 64 64" aria-hidden="true" role="img" class="iconify iconify--emojione" preserveAspectRatio="xMidYMid meet"><circle cx="32" cy="32" r="30" fill="#3a7dce"/><path fill="#fff" d="M17.6 30.7l-.3-1.4H17l-.5.5l-.1-1.3l-.6-.5l-.4.2v.2l-.7-.3l-.5-.6l1.2-1l-2-1.6l-1-3.7l7.4 5.3l4.6-1.2l-.2-.7l.9-.2l.4-1.5l-.1-.5l.3-.4l.2-1l-.2-.4l.7-.6l-.2-1.5l1.6-.7l1.3-1.3l-.1-.7l.9.5l.8-.5l.3-.8l.4.6l4.3.2l.9.8l3.5.7l.7.7l.5-.2l.5 1.7h.3l.4-.5l3.2 1.1l.2.5l.8-.2l.9.8l.9 4.9l-.8 2.7l3.4 1l.2 2.3l-.7 1.7l1 .8l-.5 2.9l-1.7 1.3l.4 2l-1 .7l-.6-.2v1.9h-.8l.3.7l-1.7.7l.5 1l-1.1 1.2l.3.3l-.7-.2l-3.2 1.9l.2-.5l-1 .2l-.2-.5l-.8.6l-.3-.1l-.5.6l-3.6-.5l-.5-.3l-.6.3l-1.3-1l.6-.6l.9-1.8v-1.1l-.7-1.6l-.8.8l-4.7-1.2l-1 .1l-.8.5l-2.3-.2v.4l-4.8-1.7v-1h-.8l-.2-2.9l-.6.2l-.9-2.1l.2.5l-1.7-1.8h1l-.3-2l.8-1.4h.5"/></svg>
        </div>
        <md-card class="md-primary" md-theme="purple-card" md-with-hover>
          <md-ripple>
            <md-card-content>
              <div>Selected year: {{year}}</div>
              <div>Max {{month}} ice volume: {{Math.max.apply(Math, values.data)}} km&sup3;</div>
              <div>Min {{month}} ice volume: {{Math.min.apply(Math, values.data)}} km&sup3;</div>
            </md-card-content>
          </md-ripple>
        </md-card>

        <div class="chart-container">
          <DoughnutChart v-on:setYear="setYear" v-on:setValue="setValue" :data="values" ></DoughnutChart>
        </div>
      </div>
      <div class="right">
        <md-radio v-for="m in months" :key="m" v-model="month" v-on:change="getDataByMonth" :value="m">{{m}}</md-radio>
      </div>

    </div>

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
      checked: false,
      global_is_exist: false,
      active: false,
      value: 0,
      values: {
        data: [],
        years: []
      },
      year: "2022",
      month: "Jan",
      processing: false,
      formdata: {},
      months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep","Oct","Nov","Dec"]
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
          }else{
            that.checked = true;
          }
        });
  },
  methods: {
    setYear(year){
      this.year = year;
    },
    setValue(val){
      this.value = val;
    },
    getMessage(){
      return `Set the volume (km^3) for ${this.month} ${this.year}`
    },
    uploadData() {
      this.processing = true;
      this.formdata = {};
      let that = this;
      axios.post('http://127.0.0.1:8011/import-dataset', this.formdata).then(
          function (response) {
            if(response.data.status){
              that.global_is_exist = true;
              that.checked = true;

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
            if(response.data.status){
              that.getDataByMonth()
            }
          });
    }
  }
}
</script>

<style scoped>
.md-radio {
  display: flex;
}
.md-theme-purple-card{
  left: 15px;
  width: 280px;
  position: absolute;
  top: 63vh;
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