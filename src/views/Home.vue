<template>
  <v-container>
      <v-row dense>
        <v-col
          v-for="(session, i) in sessions"
          :key="i"
          sm="12"
          md="4"
        >
          <v-card
            color="#952175"
            elevation="3"
            outlined
            dark
          >
            <v-card-title
              class="headline"
              v-text="'Session '+ session.id"
            >
            </v-card-title>

            <v-card-subtitle v-text="new Date(parseInt(session.created_at))"></v-card-subtitle>

            <v-card-actions>
              <v-btn
                :to="'/session/' + session.id"
                class="ml-2 mt-1"
                outlined
                rounded
              >
                LIVE
              </v-btn>
              <v-btn
                :to="'/datatable/' + session.id"
                class="ml-2 mt-1"
                outlined
                rounded
              >
                DATATABLE
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn text @click="deleteSession(session.id)"><v-icon>mdi-delete</v-icon></v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
      })
    },
    created() {
      this.setSessions();
    },
    destroyed() {
      clearTimeout(this.timeoutId);
    }
  };
</script>
