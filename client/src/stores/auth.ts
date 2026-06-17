import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const userId = ref<number | null>(null)

    function loadFromStorage() {
        const raw = localStorage.getItem('user_id')
        const n = raw ? Number.parseInt(raw, 10) : NaN
        userId.value = Number.isNaN(n) ? null : n
    }

    function login(id: number) {
        localStorage.setItem('user_id', String(id))
        userId.value = id
    }

    function logout() {
        localStorage.removeItem('user_id')
        userId.value = null
    }

    const isLoggedIn = computed(() => userId.value !== null)

    return { userId, isLoggedIn, loadFromStorage, login, logout }
})