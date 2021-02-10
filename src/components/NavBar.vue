<template>
	<v-app-bar app color="primary" dark>
    <div class="d-flex align-center">
      <v-img
        alt="Server Dashboard Logo"
        class="shrink mr-2"
        contain
        src="@/assets/logo.png"
        transition="scale-transition"
        width="40"
      />
    </div>
    <router-link :to="{name: 'Home'}"><v-toolbar-title class="white--text">PX4-AUTOPILOT</v-toolbar-title></router-link>
    <v-spacer></v-spacer>
	</v-app-bar>
</template>

<script>
export default {
	name: "NavBar",
  data: () => ({
    //
  })
};
</script>
