import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    endpoints: {
      sessions: "/api/v1/sessions/"
    },
    sessions: []
  },
  mutations: {
    'SET_SESSIONS'(state, sessions) {
      state.sessions = sessions;
    }
  },
  actions: {
    setSessions({state, commit, dispatch}) {
      axios.get(state.endpoints.sessions)
        .then(res => {
          // console.log(res);
          commit("SET_SESSIONS", res.data);
          setTimeout(() => {
            dispatch("setSessions")
          }, 5000)
        })
        .catch(err => {
          // console.log(err.message);
          setTimeout(() => {
            dispatch("setSessions")
          }, 5000)
        })
    }
  },
  getters: {
    getSessions(state) {
      return state.sessions;
    }
  },
  modules: {}
});
