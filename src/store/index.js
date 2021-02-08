import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    endpoints: {
      sessions: "/api/v1/sessions/",
      mapData: "/api/v1/session/"
    },
    sessions: [],
    mapData: {}
  },
  mutations: {
    'SET_SESSIONS'(state, sessions) {
      state.sessions = sessions;
    },
    'SET_MAP_DATA'(state, mapData) {
      state.mapData = mapData;
    }
  },
  actions: {
    setMapData({state, commit}, sessionId) {
      axios.get(state.endpoints.mapData + `${sessionId}/`)
        .then(res => {
          console.log(res.data);
          commit("SET_MAP_DATA")
        })
        .catch(err => {
          console.log(err.message);
        })
    },
  },
  getters: {
    getSessions(state) {
      return state.sessions;
    },
    getMapData(state) {
      return state.mapData;
    }
  },
  modules: {}
});
