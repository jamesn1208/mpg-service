import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'home-alt',
    component: () => import('@/views/Home.vue')
  },
  {
    name: 'home',
    path: '/home',
    component: () => import('@/views/Home.vue')
  },
  {
    name: 'not-found',
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFound.vue')
  },
]


export const router = createRouter({
  history: createWebHistory('/app'),
  routes,
})
