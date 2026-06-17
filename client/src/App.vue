<script setup lang="ts">
import {
  useRoute,
  useRouter
} from 'vue-router'
import { useColorMode } from '@vueuse/core'
import {
  computed,
  onMounted
} from 'vue'
import { toast } from 'vue-sonner'
import { Icon } from '@iconify/vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger
} from '@/components/ui/dropdown-menu'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuList
} from '@/components/ui/navigation-menu'
import { Button } from '@/components/ui/button'
import {
  movePage,
  callAPI
} from "@/lib/common"
import { useAuthStore } from '@/stores/auth'


const route = useRoute()
const router = useRouter()
const hideHeader = computed(() => Boolean(route.meta?.hideHeader))
const mode = useColorMode()
const auth = useAuthStore()


onMounted(() => {
  auth.loadFromStorage()
})

function logout() {
  try {
    callAPI('/api/v1/users/logout', 'POST')
    auth.logout()
    toast('Success', {description: 'Logged out.'})
  } catch (e) {
    toast('Failure', {description: e as string})
  }
}
</script>

<template>
  <Toaster />

  <div v-if="!hideHeader" class="flex w-full py-4 px-4 h-24 items-center justify-between border-b border-b-secondary">
    <NavigationMenu class="h-full">
      <NavigationMenuList class="h-full flex items-center">
        <RouterLink
            class="pr-2 py-3 font-bold text-xl w-max lg:px-4 lg:mr-6 lg:text-2xl rounded-2xl hover:bg-primary-foreground transition-all fade-in-out"
            to="/">
          MPG Service
        </RouterLink>
        <NavigationMenuItem>
          <RouterLink
              to="/browse"
              class="text-base rounded-2xl px-4 py-3 hover:bg-primary-foreground transition-all fade-in-out">
            Browse
          </RouterLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>

    <div class="h-full flex items-center relative">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <font-awesome-icon icon="fa-solid fa-circle-user" class="hover:scale-110 transition-all fade-in-out mr-4 text-2xl hover:cursor-pointer"/>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" class="z-50 min-w-35">
          <DropdownMenuItem v-if="!auth.isLoggedIn" @click="movePage(router, '/login')" class="hover:cursor-pointer">Login</DropdownMenuItem>
          <DropdownMenuItem v-if="auth.isLoggedIn" @click="movePage(router, '/log')" class="hover:cursor-pointer">New Log</DropdownMenuItem>
          <DropdownMenuItem v-if="auth.isLoggedIn" @click="movePage(router, `/profile`)" class="hover:cursor-pointer">Profile</DropdownMenuItem>
          <DropdownMenuItem v-if="auth.isLoggedIn" @click="logout()" class="hover:cursor-pointer" variant="destructive">Logout</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="outline" class="hover:scale-110 fade-in-out hover:cursor-pointer">
            <Icon icon="radix-icons:moon"
                  class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"/>
            <Icon icon="radix-icons:sun"
                  class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"/>
            <span class="sr-only">Toggle theme</span>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" class="z-50 min-w-35">
          <DropdownMenuItem @click="mode = 'light'" class="hover:cursor-pointer">Light</DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'dark'" class="hover:cursor-pointer">Dark</DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'auto'" class="hover:cursor-pointer">System</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </div>

  <router-view :key="route.fullPath"/>
</template>
