import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/session/:sessionId",
    name: "Session",
    component: () => import("@/views/Session.vue"),
  },
  {
    path: "/datatable/:sessionId",
    name: "DataTable",
    component: () => import("@/views/DataTable.vue"),
  }
];

const router = new VueRouter({
  mode: "history",
  // base: process.env.BASE_URL,
  routes
});

export default router;
