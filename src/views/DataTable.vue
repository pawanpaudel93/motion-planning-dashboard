<template>
  <v-container>
    <apexchart type="area" height="350" :options="getChartOptions('Local Position')" :series="seriesOne"></apexchart>
    <apexchart type="area" height="350" :options="getChartOptions('Local Velocity')" :series="seriesTwo"></apexchart>
    <v-list-item v-for="(data, name) in filteredData" v-bind:key="name">
      <v-list-item-content>
        <v-list-item-title>
          <v-card
            elevation="2"
            outlined
            shaped
            tile
          >
            <v-card-title>
              {{name[0].toUpperCase() + name.slice(1)}}
            </v-card-title>
            <v-data-table
              :headers="headers(name)"
              :items="data"
              item-key="name"
              class="elevation-1"
            >
              <template v-slot:item.timestamp="{ item }">
                <span>{{ new Date(parseInt(item.timestamp)).toGMTString() }}</span>
              </template>
            </v-data-table>
          </v-card>
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-container>
</template>

<script>
  import axios from 'axios';
  import apexchart from "vue-apexcharts"
  export default {
    name: "DataTable",
    data: () => ({
      sessionData: {},
      seriesOne: [],
      seriesTwo: [],
    }),
    components: {
      apexchart
    },
    methods: {
      getChartOptions(name) {
        return {
          chart: {
            type: 'area',
            stacked: false,
            height: 350,
            zoom: {
              type: 'x',
              enabled: true,
              autoScaleYaxis: true
            },
            toolbar: {
              autoSelected: 'zoom'
            }
          },
          dataLabels: {
            enabled: false
          },
          markers: {
            size: 0,
          },
          title: {
            text: name,
            align: 'left'
          },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              inverseColors: false,
              opacityFrom: 0.5,
              opacityTo: 0,
              stops: [0, 90, 100]
            },
          },
          yaxis: {
            labels: {
              formatter: function (val) {
                return val.toFixed(2);
              },
            },
            title: {
              text: 'value'
            },
          },
          xaxis: {
            type: 'datetime',
          },
          tooltip: {
            shared: false,
          }
        }
      },
      getData(name, arrName) {
        let data1 = [],
            data2 = [],
            data3 = [];
        for (let i = 0; i < this.sessionData[name].length; i++) {
          data1.push([parseInt(this.sessionData[name][i].timestamp), this.sessionData[name][i].value[0]])
          data2.push([parseInt(this.sessionData[name][i].timestamp), this.sessionData[name][i].value[1]])
          data3.push([parseInt(this.sessionData[name][i].timestamp), this.sessionData[name][i].value[2]])
        }
        this[arrName] = [
          {
            name: name=='localPosition'?'North':'VNorth',
            data: data1
          },
          {
            name: name=='localPosition'?'East':'VEast',
            data: data2
          },
          {
            name: name=='localPosition'?'Down':'VDown',
            data: data3
          }
        ]
      },
      headers (name) {
        let text1, text2, text3;
        let headers = [
          {
            text: 'Timestamp',
            align: 'start',
            sortable: true,
            value: 'timestamp',
          },
        ]
        if (name.includes('global')) {
          text1 = "Longitude(degree)"
          text2 = "Latitude(degree)"
          text3 = "Altitude(meter)"
        } else if (name == "localPosition") {
          text1 = "North(meter)"
          text2 = "East(meter)"
          text3 = "Down(meter)"
        } else {
          text1 = "VNorth(meter/second)"
          text2 = "VEast(meter/second)"
          text3 = "VDown(meter/second)"
        }
        headers.push(...[
          { text: text1, value: 'value[0]' },
          { text: text2, value: 'value[1]' },
          { text: text3, value: 'value[2]' },
        ])
        return headers
      },
    },
    computed: {
      filteredData() {
        let notAllowed = ['movement']
        return Object.keys(this.sessionData)
        .filter(key => !notAllowed.includes(key))
        .reduce((obj, key) => {
          obj[key] = this.sessionData[key];
          return obj;
        }, {});
      },
    },
    created() {
      axios.get(this.$store.state.endpoints.tableData + `${this.$route.params.sessionId}`)
        .then(res => {
          this.sessionData = res.data;
          this.getData('localPosition', 'seriesOne');
          this.getData('localVelocity', 'seriesTwo');
        })
        .catch(err => {
          console.log(err)
        })
    }
  };
</script>
