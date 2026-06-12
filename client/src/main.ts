import Sonner from 'vue-sonner'
import { createApp } from 'vue'
import { router } from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    faCloudBolt,
    faChevronLeft,
    faCircleUser,
    faHurricane
} from '@fortawesome/free-solid-svg-icons'
import App from './App.vue'
import './style.css'
import 'vue-sonner/style.css'


library.add(faCloudBolt, faChevronLeft, faCircleUser, faHurricane)

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(Sonner)
app.mount('#app')
