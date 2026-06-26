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
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import { callAPI } from "@/lib/common.ts";
import { toast } from "vue-sonner";
import PageBreak from "@/components/PageBreak.vue"
import { Button } from "@/components/ui/button";
import { Icon } from '@iconify/vue';
import { useAuthStore } from "@/stores/auth.ts"
import {Input} from "@/components/ui/input";
import {Label} from "@/components/ui/label";

const registration: Ref<string | null> = ref(null)
const vehicles: Ref<any[] | null> = ref(null)
const data: Ref<any[] | null> = ref(null)
const page: Ref<number> = ref(1)
const pageSize: Ref<number> = ref(10)
const totalRecords: Ref<number> = ref(10)
const auth = useAuthStore()


function populateData() {
  if (!auth.isLoggedIn) {
    return
  }

  let path = "/api/v1/mpg"
  const query = new URLSearchParams()

  if (typeof registration.value === "string") {
    path = `/api/v1/mpg/${registration.value}`
  }
  query.set('offset', (page.value - 1).toString())
  if (pageSize.value < 1 || pageSize.value > 250) {
    return
  }
  query.set('limit', pageSize.value.toString())

  path = `${path}?${query}`

  callAPI(path, 'GET')
      .then((json) => {
        data.value = json.data
        totalRecords.value = json.total
        pageSize.value = json.size
        page.value = json.page
      }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })
}

onMounted(() => {
  // Get list of vehicles registered to the user
  callAPI('/api/v1/vehicles', 'GET')
    .then((json) => {
      vehicles.value = json
    }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })

  // Get initial MPG data
  populateData()
})

watch(pageSize, (newPageSize) => {
  if (newPageSize > 250) {
    pageSize.value = 250
  }
  if (newPageSize < 1) {
    pageSize.value = 1
  }
  page.value = 1
  populateData()
})

// @ts-ignore
watch([page, registration], (_: Ref<string | null | number>) => {
  populateData()
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
      <div class="w-[90%] mt-6 inline-flex gap-2 items-center outline-destructive outline-2 outline-dashed p-2 rounded-xl lg:w-fit" v-if="(!vehicles || vehicles.length === 0) && auth.isLoggedIn">
        <Icon icon="material-symbols:warning-rounded" class="scale-200 xl:scale-125"/>
        <p class="brightness-75">You have not registered any vehicles yet! <RouterLink to="/profile" class="underline">Add one here</RouterLink></p>
      </div>
      <div class="flex flex-col mt-6 gap-2">
        <Label for="pagination-size">Page size</Label>
        <Input id="pagination-size" class="w-15 text-center appearance-none font-bold" type="number" v-model="pageSize" max="250" min="1" />
      </div>
      <div class="flex flex-col gap-6 mt-4">
        <Pagination
            v-model:page="page"
            :items-per-page="pageSize"
            :total="totalRecords"
        >
          <PaginationContent v-slot="{ items }">
            <PaginationPrevious />
            <template v-for="(item, index) in items" :key="index">
              <PaginationItem
                  v-if="item.type === 'page'"
                  :value="item.value"
                  :is-active="item.value === page"
              >
                {{ item.value }}
              </PaginationItem>
            </template>
            <PaginationEllipsis v-if="items.length > 0" />
            <PaginationNext />
          </PaginationContent>
        </Pagination>
      </div>
      <PageBreak class="mt-6 mb-8"/>

      <div v-if="!auth.isLoggedIn" class="flex flex-cols-2 gap-2 justify-center items-center">
        <Icon icon="material-symbols:warning-rounded" class="scale-120 brightness-75" />
        <h2 class="brightness-75">You are not logged in.</h2>
      </div>

      <div v-if="(!data || data.length === 0) && auth.isLoggedIn" class="flex flex-cols-2 gap-2 justify-center items-center">
        <Icon icon="material-symbols:warning-rounded" class="scale-120 brightness-75" />
        <h2 class="brightness-75">No more data.</h2>
      </div>
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
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-200 dark:bg-violet-500">
              <h3 class="font-bold">MPG</h3>
              <p class="w-full place-self-center">
                {{ log.mpg }}mi/G
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-200 dark:bg-violet-500">
              <h3 class="font-bold">Litres</h3>
              <p class="w-full place-self-center">
                {{ log.litres }}L
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-200 dark:bg-violet-500">
              <h3 class="font-bold">Miles</h3>
              <p class="w-full place-self-center">
                {{ log.miles }}mi
              </p>
            </div>
            <div class="grid grid-cols-1 gap-0 w-full p-4 rounded-3xl bg-violet-200 dark:bg-violet-500">
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
