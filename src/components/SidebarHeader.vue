<template>
  <div class="header">
    <img src="@/assets/logo.png" class="logo">
    <router-link :to="{name: 'Home'}"><v-toolbar-title class="white--text">PX4-AUTOPILOT</v-toolbar-title></router-link>
  </div>
</template>

<style>
.header {
  text-align: center;
  padding: 1rem;
}
.logo {
  width: 80px;
}
</style>