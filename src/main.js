import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;
// axios.defaults.baseURL = process.env.VUE_APP_BASEURL;
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");
