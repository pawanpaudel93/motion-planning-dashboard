<template>
  <div class="header">
    <router-link :to="{name: 'Home'}"><img src="@/assets/logo.png" class="logo"></router-link>
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