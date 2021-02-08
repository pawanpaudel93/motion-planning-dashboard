<template>

</template>
<script>
  import {mapGetters} from 'vuex';
  export default {
    name: "Session",
    computed: {
      ...mapGetters({
        mapData: "getMapData",
      })
    },
    created() {
      this.$store.dispatch("setMapData", this.$route.params.sessionId)
    }
  }
</script>