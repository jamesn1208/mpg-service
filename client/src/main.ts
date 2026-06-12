import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import NotFound from './views/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'home-alt',
    component: Home
  },
  {
    name: 'home',
    path: '/home',
    component: Home
  },
  {
    name: 'not-found',
    path: '/:pathMatch(.*)*',
    component: NotFound
  },
]

export const router = createRouter({
  history: createWebHistory('/app'),
  routes,
})

createApp(App)
  .use(router)
  .mount('#app')
