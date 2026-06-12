import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('@/views/Login.vue'),
        meta: { hideHeader: true }
    },
    {
        path: '/browse',
        name: 'Browse',
        component: () => import('@/views/Browse.vue')
    },
    {
        path: '/sign-up',
        name: 'Sign Up',
        component: () => import('@/views/SignUp.vue'),
        meta: { hideHeader: true }
    },
    {
        path: '/users/:id(\\d+)',
        name: 'User Profile',
        component: () => import('@/views/UserProfile.vue'),
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'Not Found',
        component: () => import('@/views/404.vue'),
    }
]

export const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
})
