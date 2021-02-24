import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import vuetify from "@/plugins/vuetify";
import VueProgressBar from 'vue-progressbar'
import 'leaflet/dist/leaflet.css';

Vue.config.productionTip = false;
// axios.defaults.baseURL = process.env.VUE_APP_BASEURL;
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const options = {
  color: 'rgb(143, 255, 199)',
  thickness: '2px',
  transition: {
    speed: '1.5s',
    opacity: '0.6s',
    termination: 400
  },
}
Vue.use(VueProgressBar, options);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
