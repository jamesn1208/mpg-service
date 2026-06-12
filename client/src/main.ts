import './assets/main.css'

import { createApp } from 'vue'
import { router } from '@/router'
import App from './App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {faCloudBolt, faChevronLeft, faCircleUser, faHurricane} from '@fortawesome/free-solid-svg-icons'


library.add(faCloudBolt, faChevronLeft, faCircleUser, faHurricane)

createApp(App)
  .component('font-awesome-icon', FontAwesomeIcon)
  .use(router)
  .mount('#app')
