<script setup lang="ts">
import PageBreak from "@/components/PageBreak.vue";
import {
  ref,
  type Ref,
  onMounted
} from "vue";
import { toast } from "vue-sonner"
import { Skeleton } from "@/components/ui/skeleton";
import { callAPI } from "@/lib/common.ts"
import { useAuthStore } from "@/stores/auth.ts";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { Icon } from '@iconify/vue';

document.title = 'MPG Service | Home'
const data: Ref<any[] | null> = ref(null)
const auth = useAuthStore()

const populateData = () => {
  if (!auth.isLoggedIn) {
    return
  }

  callAPI('/api/v1/metrics', 'GET')
      .then((json) => {
        data.value = json
      }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })
}

onMounted(() => {
  populateData()
})
</script>

<template>
  <main>
    <div class="w-full pb-20">
      <div class="w-full flex justify-center items-center mt-12 mb-12">
        <img
          loading="eager"
          alt="Website logo"
          class="h-5/6 w-5/6 lg:h-1/2 lg:w-1/2 xl:h-1/3 xl:w-1/3"
          src="../assets/logo.svg"
        />
      </div>
      <PageBreak />
      <h2 class="text-5xl mt-8 mb-4 w-full text-center">Statistics</h2>
      <div class="w-full flex justify-center">
        <div class="inline-flex items-center gap-2 mt-6" v-if="!auth.isLoggedIn">
          <Icon icon="material-symbols:warning-rounded" class="scale-120 brightness-75" />
          <h2 class="brightness-75">You are not logged in.</h2>
        </div>
        <div class="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-8 xl:grid-cols-3 xl:gap-10 mt-4 place-items-center w-full" v-if="auth.isLoggedIn">
          <!-- Skeleton placeholders -->
          <div
              v-if="data === null"
              v-for="d in [1, 2, 3, 4, 5, 6, 7, 8, 9]"
              :key="d"
          >
            <Skeleton class="w-[90%] lg:min-w-md lg:min-h-60 rounded-3xl" />
          </div>
          <!-- Real data -->
          <div
              class="p-4 w-[90%] h-fit lg:min-w-md lg:min-h-60 rounded-3xl bg-secondary grid grid-cols-1 gap-4 text-center"
              v-for="d in data"
              :key="d.title"
              v-if="data != null"
            >
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger as-child>
                  <h3 class="text-2xl lg:text-3xl font-extralight">{{ d.title }}</h3>  <!-- Title -->
                </TooltipTrigger>
                <TooltipContent>
                  <p>{{ d.description }}</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <div class="flex w-full justify-center">  <!-- Value -->
              <p class="py-4 px-10 text-4xl lg:text-7xl font-bold rounded-full bg-card w-fit h-fit">{{ d.value }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
