<template>
  <div id='myDiv'></div>
</template>
<script>
  import {mapGetters} from 'vuex';
  import Plotly from 'plotly.js-dist'
  import axios from 'axios'
  export default {
    name: "Session",
    data: () => ({
      mapData: {}
    }),
    computed: {

    },
    methods: {
      setMapData() {
        axios.get(this.$store.state.endpoints.mapData + `${this.$route.params.sessionId}/`)
          .then(res => {
            console.log(res.data)
            this.mapData = res.data;
            var data = [
              {
                z: this.mapData.grid,
                colorscale: 'Viridis',
                showscale: false,
                type: 'heatmap'
              }
            ];
            for (let i=0; i<this.mapData.edges.length; i++) {
              let [p1, p2] = this.mapData.edges[i]
              data.push({
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
            }
            var layout = {
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
            Plotly.newPlot('myDiv', data, layout);
          })
          .catch(err => {
            console.log(err.message);
          })
      },
    },
    created() {
      this.setMapData();
    },
  }
</script>