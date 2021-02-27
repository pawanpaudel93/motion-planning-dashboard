import Vue from "vue";
import VueRouter from 'vue-router'
import DashboardLayout from '@/layout/DashboardLayout.vue'
// GeneralViews
import NotFound from '@/views/NotFoundPage.vue'

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/admin/home'
  },
  {
    path: '/admin',
    component: DashboardLayout,
    redirect: '/admin/home',
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import("@/views/Home.vue"),
      },
      {
        path: 'user',
        name: 'User',
        component: () => import("@/views/UserProfile.vue"),
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
    ]
  },
  { path: '*', component: NotFound }
]

export default new VueRouter({
  // mode: 'history',
  routes, // short for routes: routes
  linkActiveClass: 'nav-item active',
  scrollBehavior: (to) => {
    if (to.hash) {
      return {selector: to.hash}
    } else {
      return { x: 0, y: 0 }
    }
  }
})
