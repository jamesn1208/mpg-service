import './assets/main.css'

import { createApp } from 'vue'
import { router } from '@/router'
import App from './App.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

createApp(App)
  .component('font-awesome-icon', FontAwesomeIcon)
  .use(router)
  .mount('#app')
