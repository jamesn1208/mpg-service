<script setup lang="ts">
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  ref,
  type Ref,
  watch,
  onMounted,
} from 'vue'
import { callAPI } from "@/lib/common.ts";
import { toast } from "vue-sonner";
import PageBreak from "@/components/PageBreak.vue"
import {Button} from "@/components/ui/button";
import { Icon } from '@iconify/vue';

const registration: Ref<string | null> = ref(null)
const vehicles: Ref<any[] | null> = ref(null)
const data: Ref<any[] | null> = ref(null)

onMounted(() => {
  // Get list of vehicles registered to the user
  callAPI('/api/v1/vehicles', 'GET')
    .then((json) => {
      vehicles.value = json
    }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })

  // Get initial MPG data
  callAPI('/api/v1/mpg', 'GET')
    .then((json) => {
      data.value = json
    }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })
})

watch(registration, (reg: Ref<string | null>) => {
  // Update data.value here
  console.log(reg)
})

document.title = 'MPG Service | Browse'
</script>

<template>
  <main>
    <div class="flex flex-col justify-center items-center mt-12 mb-12">
      <div class="flex justify-center flex-col w-full text-center mb-6">
        <h2 class="text-3xl">Browse previous refueling data</h2>
        <p class="brightness-75 text-md">Refueling logs are sorted by date descending, and can be filtered by registration.</p>
      </div>
      <div class="flex justify-center gap-2">
        <Select v-model="registration">
          <SelectTrigger>
            <SelectValue placeholder="All Vehicles" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem
                v-if="vehicles != null"
                v-for="vehicle in vehicles"
                :disabled="vehicles.length === 0"
                :value="vehicle.registration">
              {{ vehicle.registration }}
            </SelectItem>
          </SelectContent>
        </Select>
        <Button
            variant="destructive"
            class="hover:cursor-pointer"
            @click="() => {registration = null}"
            :disabled="registration === null"
        >
          Clear
        </Button>
      </div>
      <PageBreak class="mt-8 mb-8"/>

      <div class="grid grid-cols-1 gap-14 lg:grid-cols-2 lg:gap-8 xl:grid-cols-3 xl:gap-10 mt-4 place-items-center w-full mb-16">
        <div
            v-for="log in data"
            class="p-4 w-[90%] h-fit lg:min-w-md lg:min-h-60 rounded-3xl bg-secondary grid grid-cols-1 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold">{{ log.registration }}</p>
            <div class="flex items-center justify-center gap-1">
              <Icon icon="formkit:date"/>
              <p class="text-sm">{{ log.date }}</p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4 w-full mt-2">
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-500">
              <h3 class="font-bold">MPG</h3>
              <p class="w-full place-self-center">
                {{ log.mpg }}mi/G
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-500">
              <h3 class="font-bold">Litres</h3>
              <p class="w-full place-self-center">
                {{ log.litres }}L
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-500">
              <h3 class="font-bold">Miles</h3>
              <p class="w-full place-self-center">
                {{ log.miles }}mi
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-500">
              <h3 class="font-bold">Cost</h3>
              <p class="w-full place-self-center">
                £{{ log.total_cost }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
