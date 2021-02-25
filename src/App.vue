<template>
  <v-app>
    <v-main>
      <VdDashboard
        pageBackground="#f8f8f8"
        sidebarHeaderHeight="175px"
        headerBackground="white"
        sidebarBackground="purple"
      >
        <template v-slot:main-content>
          <router-view />
        </template>
        <template v-slot:header-content>
          <HeaderItems></HeaderItems>
        </template>
        <template v-slot:sidebar-header>
          <SidebarHeader></SidebarHeader>
        </template>
        <template v-slot:sidebar-content>
          <SidebarItems></SidebarItems>
        </template>
      </VdDashboard>
    </v-main>
    <vue-progress-bar></vue-progress-bar>
  </v-app>
</template>

<script>
  import NavBar from "@/components/NavBar";
  import HeaderItems from '@/components/HeaderItems';
  import SidebarHeader from '@/components/SidebarHeader';
  import SidebarItems from '@/components/SidebarItems';
  export default {
    name: "App",
    components: {
      NavBar,
      HeaderItems,
      SidebarHeader,
      SidebarItems,
    },
    mounted () {
      //  [App.vue specific] When App.vue is finish loading finish the progress bar
      this.$Progress.finish()
    },
    created () {
      //  [App.vue specific] When App.vue is first loaded start the progress bar
      this.$Progress.start()
      //  hook the progress bar to start before we move router-view
      this.$router.beforeEach((to, from, next) => {
        //  does the page we want to go to have a meta.progress object
        if (to.meta.progress !== undefined) {
          let meta = to.meta.progress
          // parse meta tags
          this.$Progress.parseMeta(meta)
        }
        //  start the progress bar
        this.$Progress.start()
        //  continue to next page
        next()
      })
      //  hook the progress bar to finish after we've finished moving router-view
      this.$router.afterEach((to, from) => {
        //  finish the progress bar
        this.$Progress.finish()
      })
    }
  };
</script>
