<script setup lang="ts">
import NewVehicleForm from "@/components/NewVehicleForm.vue";
import { useAuthStore } from "@/stores/auth.ts";
import {Icon} from "@iconify/vue";

const auth = useAuthStore()

document.title = 'MPG Service | New Vehicle'
</script>

<template>
  <div class="flex w-full flex-col items-center justify-center mt-20 pb-30">
    <div class="w-[90%] xl:w-[30%]">
      <div v-if="!auth.isLoggedIn" class="flex flex-cols-2 gap-2 justify-center items-center">
        <Icon icon="material-symbols:warning-rounded" class="scale-120 brightness-75" />
        <h2 class="brightness-75">You are not logged in.</h2>
      </div>
      <NewVehicleForm v-if="auth.isLoggedIn"/>
    </div>
  </div>
</template>
