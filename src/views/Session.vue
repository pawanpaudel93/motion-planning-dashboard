<template>
  <v-container>
    <v-overlay :value="loading">
      Loading...<br>
      <v-progress-circular
        :size="70"
        :width="7"
        color="blue"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-row v-if="!loading">
      <v-col>
        <Plotly :data="data" :layout="layout" :display-mode-bar="true"></Plotly>
      </v-col>
      <v-col>
        <v-simple-table v-if="Object.keys(sessionData).length !==0">
          <template v-slot:default>
            <thead>
              <tr>
                <th class="text-left">
                  Name
                </th>
                <th class="text-left">
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(value, key) in filteredSession"
                :key="key"
              >
                <td>{{ key }}</td>
                <td>{{ value }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>  
  </v-container>
</template>
<script>
  import { Plotly } from 'vue-plotly'
  import axios from 'axios'
  export default {
    name: "Session",
    components: {
      Plotly
    },
    data: () => ({
      data: [],
      layout: {},
      sessionData: {},
      loading: true,
      timeoutId: null,
      displayed: false
    }),
    computed: {
      filteredSession() {
        let notAllowed = ['session', 'movement']
        return Object.keys(this.sessionData)
        .filter(key => !notAllowed.includes(key))
        .reduce((obj, key) => {
          obj[key] = this.sessionData[key];
          return obj;
        }, {});
      }
    },
    methods: {
      getMapData() {
        axios.get(this.$store.state.endpoints.mapData + `${this.$route.params.sessionId}/`)
          .then(res => {
            console.log(res.data)
            let mapData = res.data;
            this.data.push(
              {
                z: mapData.grid,
                colorscale: 'Viridis',
                showscale: false,
                type: 'heatmap'
              }
            )
            this.layout = {
              title: 'Session Data',
              width: 700,
              height: 700,
              showlegend: false,
              xaxis: {
                title: {
                  text: 'EAST',
                  font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                  }
                },
              },
              yaxis: {
                title: {
                  text: 'NORTH',
                  font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                  }
                }
              }
            };
            mapData.edges.forEach((edge) => {
              let [p1, p2] = edge;
              this.data.push({
                x: [p1[1], p2[1]],
                y: [p1[0], p2[0]],
                mode: "lines",
                line: {
                  color: "#001FFF",
                  shape: 'spline',
                  width: 2.5
                },
                type: 'scatter'
              })
            });
            this.loading = false;
            this.getSessionData();
          })
          .catch(err => {
            console.log(err.message);
          })
      },
      getSessionData() {
        axios.get(this.$store.state.endpoints.sessionData + `${this.$route.params.sessionId}`)
          .then(res => {
            console.log(res.data)
            this.sessionData = res.data;
            if (!this.loading && !this.displayed && this.sessionData.session.start != null) {
              let {goal, start} = this.sessionData.session;
              this.data.push({
                x: [start[1]],
                y: [start[0]],
                mode: "markers",
                marker: {
                  color: "#FF0000",
                  size: 10,
                },
                type: 'scatter'
              })
              this.data.push({
                x: [goal[1]],
                y: [goal[0]],
                mode: "markers",
                marker: {
                  color: "#FF0000",
                  size: 10,
                  symbol: 'x'
                },
                type: 'scatter'
              })
              this.displayed = true;
            }
            let movementLength = this.sessionData.movement.length;
            if (movementLength != 0) {
              if (this.sessionData.session.isFinished) {
                let xAxis = [],
                    yAxis = [];
                this.sessionData.movement.forEach((item) => {
                  xAxis.push(item[1]);
                  yAxis.push(item[0]);
                })
                this.data.push({
                  x: xAxis,
                  y: yAxis,
                  mode: "lines",
                  line: {
                    color: "#00FF00",
                    shape: 'spline',
                    width: 2.5
                  },
                  type: 'scatter'
                })
              } else {
                let point = this.sessionData.movement[movementLength-1]
                this.data.push({
                  x: [point[1]],
                  y: [point[0]],
                  mode: "markers",
                  marker: {
                    color: "#00FF00",
                    size: 7,
                    symbol: 'star-diamond'
                  },
                  type: 'scatter'
                })
              }
            }
            if (!this.sessionData.session.isFinished) {
              clearTimeout(this.timeoutId);
              this.timeoutId = setTimeout(() => {
                this.getSessionData();
              }, 5000)
            }
          })
          .catch(err => {
            console.log(err.message)
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => {
              this.getSessionData();
            }, 5000)
          })
      }
    },
    created() {
      this.getMapData();
    },
    destroyed() {
      clearTimeout(this.timeoutId);
    }
  }
</script>