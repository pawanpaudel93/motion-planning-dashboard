/*!

 =========================================================
 * Vue Light Bootstrap Dashboard - v2.0.0 (Bootstrap 4)
 =========================================================

 * Product Page: http://www.creative-tim.com/product/light-bootstrap-dashboard
 * Copyright 2019 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/light-bootstrap-dashboard/blob/master/LICENSE.md)

 =========================================================

 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

 */
import Vue from 'vue'
import App from './App.vue'
import router from "./router";
import store from "./store";
import axios from "axios";
import VueProgressBar from 'vue-progressbar'
import LightBootstrap from './light-bootstrap-main'
import vuetify from "@/plugins/vuetify";

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

Vue.use(LightBootstrap);
Vue.use(VueProgressBar, options);

new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store,
  vuetify
})
