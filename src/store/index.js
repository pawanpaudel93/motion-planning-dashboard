import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    endpoints: {
      sessions: "/api/v1/sessions/",
      mapData: "/api/v1/session/",
      sessionData: "/api/v1/session-data/",
      tableData: "/api/v1/table-data/"
    },
    sessions: [],
  },
  mutations: {
    'SET_SESSIONS'(state, sessions) {
      state.sessions = sessions;
    },
  },
  actions: {
    
  },
  getters: {
    getSessions(state) {
      return state.sessions;
    },
  },
  modules: {}
});
