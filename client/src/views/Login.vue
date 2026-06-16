<script setup lang="ts">
import { Fuel } from "lucide-vue-next"
import LoginForm from "@/components/LoginForm.vue"

document.title = 'MPG Service | Login'
</script>

<template>
  <div class="bg-background flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
    <div class="flex w-full max-w-sm flex-col gap-6">
      <RouterLink to="/" class="flex items-center gap-2 self-center font-medium">
        <div class="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
          <Fuel class="size-4" />
        </div>
        MPG Service
      </RouterLink>
      <LoginForm/>
    </div>
  </div>
</template>
