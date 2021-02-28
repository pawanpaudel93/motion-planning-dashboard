<template>
  <div class="content">
    <div class="container-fluid">
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
          <v-card
            elevation="5"
            outlined
            shaped
            tile
          >
            <Plotly :data="data.concat(movement)" :layout="layout" :display-mode-bar="true"></Plotly>
          </v-card>
        </v-col>
        <v-col>
          <v-card
            elevation="5"
            outlined
            shaped
            tile
            v-if="Object.keys(sessionData).length !==0"
          >
            <v-simple-table>
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
                    <td :inner-html.prop="value|displayValue(key)"></td>
                  </tr>
                </tbody>
              </template>
            </v-simple-table>
          </v-card>
        </v-col>
      </v-row>
      <v-card
        elevation="5"
        outlined
        shaped
        tile
        class="mt-3 mb-3"
      >
        <l-map style="height: 600px" :zoom="map.zoom" :center="map.center" v-if="isFinished" ref="mymap">
          <l-tile-layer :url="map.url" subdomains="map.subdomains"></l-tile-layer>
          <l-marker :lat-lng="map.start" v-if="map.start.length > 0">
            <l-icon
              :icon-anchor="map.staticAnchor"
              class-name="someExtraClass"
            >
              <div class="headline">
                Start
              </div>
            </l-icon>
          </l-marker>
          <l-marker :lat-lng="map.goal" v-if="map.goal.length > 0">
            <l-icon
              :icon-anchor="[16, 37]"
              class-name="someExtraClass"
            >
              <div class="headline">
                Goal
              </div>
            </l-icon>
          </l-marker>
          <l-polyline :lat-lngs="map.polyline.latlngs" :color="map.polyline.color"></l-polyline>
        </l-map>
      </v-card>
    </div>
  </div>
</template>

<script>
  import { Plotly } from 'vue-plotly'
  import L from 'leaflet';
  import 'leaflet-fullscreen/dist/Leaflet.fullscreen'
  import axios from 'axios'
  import 'leaflet/dist/leaflet.css';
  import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';
  import { LMap, LTileLayer, LMarker, LPolyline, LIcon } from 'vue2-leaflet';
  export default {
    name: "Session",
    components: {
      Plotly,
      LMap,
      LTileLayer,
      LMarker,
      LPolyline,
      LIcon
    },
    data: () => ({
      data: [],
      movement: [],
      layout: {},
      sessionData: {},
      isFinished: false,
      map: {
        center: [37.792480, -122.397450],
        url: "http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}",
        zoom: 17,
        bounds: null,
        polyline: {
          latlngs: [],
          color: 'green'
        },
        staticAnchor: [16, 37],
        start: [],
        goal: [],
      },
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
            let mapData = res.data;
            this.loading = false;
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
            this.getSessionData();
          })
          .catch(err => {
            console.log(err.message);
          })
      },
      getSessionData() {
        axios.get(this.$store.state.endpoints.sessionData + `${this.$route.params.sessionId}`)
          .then(res => {
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
                text: ['Start'],
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
                text: ['Goal',],
                type: 'scatter'
              })
              this.displayed = true;
            }
            let movementLength = this.sessionData.movement.length;
            if (movementLength != 0) {
              if (this.sessionData.session.isFinished) {
                this.isFinished = true;
                let xAxis = [],
                    yAxis = [];
                this.sessionData.movement.forEach((item) => {
                  xAxis.push(item[1]);
                  yAxis.push(item[0]);
                })
                this.movement = [{
                  x: xAxis,
                  y: yAxis,
                  mode: "markers",
                  type: 'scatter',
                  marker: {
                    color: "#00FF00",
                    size: 7,
                    symbol: 'star-diamond'
                  },
                }]
                this.getPositions();
              } else {
                let point = this.sessionData.movement[movementLength-1]
                this.movement.push({
                  x: [point[1]],
                  y: [point[0]],
                  mode: "markers",
                  type: 'scatter',
                  marker: {
                    color: "#00FF00",
                    size: 7,
                    symbol: 'star-diamond'
                  },
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
            console.log(err)
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => {
              this.getSessionData();
            }, 5000)
          })
      },
      getPositions() {
         axios.get(this.$store.state.endpoints.globalPosition + `${this.$route.params.sessionId}`)
          .then(res => {
            let length = res.data.globalPosition.length
            this.map.start = [res.data.globalPosition[0].value[1], res.data.globalPosition[0].value[0]]
            this.map.goal = [res.data.globalPosition[length-1].value[1], res.data.globalPosition[length-1].value[0]]
            for(let i = 0; i < length; i++) {
              this.map.polyline.latlngs.push([res.data.globalPosition[i].value[1], res.data.globalPosition[i].value[0]])
            }
            let map = this.$refs.mymap.mapObject;
            map.addControl(new window.L.Control.Fullscreen());
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    filters: {
      displayValue: function (value, type) {
        if (type.includes('global')) {
          return `Longitude: ${value[0]} <br>Latitude: ${value[1]}<br> Altitude: ${value[2]}`
        } else if (type == 'localPosition') {
          return `North: ${value[0]}<br> East: ${value[1]}<br> Down: ${value[2]}`
        } else {
          return `VNorth: ${value[0]}<br> VEast: ${value[1]}<br> VDown: ${value[2]}`
        }
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

<style>
  .someExtraClass {
    background-color: aqua;
    padding: 10px;
    border: 1px solid #333;
    border-radius: 0 20px 20px 20px;
    box-shadow: 5px 3px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
    width: auto !important;
    height: auto !important;
    margin: 0 !important;
  }
</style>