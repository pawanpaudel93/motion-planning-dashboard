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
    <v-toolbar-title>PX4-AUTOPILOT</v-toolbar-title>
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
