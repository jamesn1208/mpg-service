<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useColorMode } from '@vueuse/core'
import { computed, ref, onMounted } from 'vue'
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
  NavigationMenuLink,
  NavigationMenuList
} from '@/components/ui/navigation-menu'
import { Button } from '@/components/ui/button'
import { movePage, callAPI } from "@/lib/common.ts"
import Cookies from 'js-cookie'


const token = ref('')
const route = useRoute()
const hideHeader = computed(() => Boolean(route.meta?.hideHeader))
const mode = useColorMode()


onMounted(() => {
  token.value = Cookies.get('X-Auth-Token') || ''
})

function logout() {
  try {
    callAPI('/api/v1/users/logout', 'POST')
    toast('Success', {description: 'Logged out.'})
  } catch (e) {
    toast('Failure', {description: e as string})
  }
}
</script>

<template>
  <Toaster />

  <div v-if="!hideHeader" class="flex w-full py-4 px-6 h-24 items-center justify-between border-b border-b-secondary">
    <NavigationMenu class="h-full">
      <NavigationMenuList class="h-full flex items-center">
        <a class="mr-5 pr-4 font-bold text-2xl" href="/">MPG Service</a>
        <NavigationMenuItem>
          <NavigationMenuLink href='/browse' class="text-base pr-5 pl-5">Browse</NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>

    <div class="h-full flex items-center relative">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <font-awesome-icon icon="fa-solid fa-circle-user" class="hover:scale-110 transition-all fade-in-out mr-4 text-2xl hover:cursor-pointer"/>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start" class="z-50 min-w-[140px]">
          <DropdownMenuItem v-if="!token" @click="movePage('/login')" class="hover:cursor-pointer">Login</DropdownMenuItem>
          <DropdownMenuItem v-if="token" @click="movePage('/create')" class="hover:cursor-pointer">New Log</DropdownMenuItem>
          <DropdownMenuItem v-if="token" @click="movePage(`/profile`)" class="hover:cursor-pointer">Profile</DropdownMenuItem>
          <DropdownMenuItem v-if="token" @click="logout()" class="hover:cursor-pointer">Logout</DropdownMenuItem>
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
        <DropdownMenuContent align="start" class="z-50 min-w-[140px]">
          <DropdownMenuItem @click="mode = 'light'">Light</DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'dark'">Dark</DropdownMenuItem>
          <DropdownMenuItem @click="mode = 'auto'">System</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </div>

  <router-view :key="route.fullPath"/>
</template>

<style>
</style>
