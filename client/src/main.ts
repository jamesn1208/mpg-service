import Sonner from 'vue-sonner'
import { createApp } from 'vue'
import { router } from './router'
import { createPinia } from 'pinia'
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
const pinia = createPinia()

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.use(pinia)
app.use(Sonner)
app.mount('#app')
