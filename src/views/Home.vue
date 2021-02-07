<template>
  <v-container>
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
                ></v-card-title>

                <v-card-subtitle v-text="Date(session.created_at)"></v-card-subtitle>

                <v-card-actions>
                  <v-btn
                    class="ml-2 mt-5"
                    outlined
                    rounded
                  >
                    VIEW
                  </v-btn>
                </v-card-actions>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>

<script>
  import { mapGetters } from 'vuex';
  export default {
    name: "Home",
    data: () => ({

    }),
    computed: {
      ...mapGetters({
        sessions: 'getSessions',
      }),
    },
    created() {
      this.$store.dispatch('setSessions');
    }
  };
</script>
