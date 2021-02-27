<template>
  <div class="content">
    <div class="container-fluid">
      <v-row dense>
        <v-col
          v-for="(session, i) in sessions"
          :key="i"
          cols="4"
        >
          <v-card
            color="#952175"
            elevation="3"
            outlined
            dark
          >
            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title
                  class="headline"
                  v-text="'Session '+ session.id"
                >
                </v-card-title>

                <v-card-subtitle v-text="Date(session.created_at)"></v-card-subtitle>

                <v-card-actions>
                  <v-btn
                    :to="'/session/' + session.id"
                    class="ml-2 mt-5"
                    outlined
                    rounded
                  >
                    LIVE
                  </v-btn>
                  <v-btn
                    :to="'/datatable/' + session.id"
                    class="ml-2 mt-5"
                    outlined
                    rounded
                  >
                    DATATABLE
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn text @click="deleteSession(session.id)"><v-icon>mdi-delete</v-icon></v-btn>
                </v-card-actions>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';
  import axios from 'axios';
  export default {
    name: "Home",
    data: () => ({
      timeoutId: null,
    }),
    methods: {
      setSessions() {
        axios.get(this.$store.state.endpoints.sessions)
        .then(res => {
          // console.log(res);
          this.$store.commit("SET_SESSIONS", res.data);
          clearTimeout(this.timeoutId);
          this.timeoutId = setTimeout(() => {
            this.setSessions();
          }, 5000)
        })
        .catch(err => {
          // console.log(err.message);
          clearTimeout(this.timeoutId);
          this.timeoutId = setTimeout(() => {
            this.setSessions();
          }, 5000)
        })
      },
      deleteSession(sessionId) {
        axios.delete(this.$store.state.endpoints.sessions + `${sessionId}/`)
          .then(res => {
            let id = this.sessions.map(item => item.id).indexOf(sessionId);
						if (id != -1) {
							this.sessions.splice(id, 1);
						}
          })
          .catch(err => {
            console.log(err.message)
          })
      }
    },
    computed: {
      ...mapGetters({
        sessions: 'getSessions',
      }),
    },
    created() {
      this.setSessions();
    },
    destroyed() {
      clearTimeout(this.timeoutId);
    }
  };
</script>
