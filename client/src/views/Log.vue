<script setup lang="ts">
import type { DateValue } from '@internationalized/date'
import {
  DateFormatter,
  getLocalTimeZone,
  today
} from '@internationalized/date'
import { CalendarIcon } from '@lucide/vue'
import { cn } from '@/lib/utils'
import { Calendar } from '@/components/ui/calendar'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  onMounted,
  ref,
  computed,
  type Ref,
  watch
} from 'vue'
import { useRouter } from 'vue-router'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import {
  callAPI,
  movePage,
  sleep
} from "@/lib/common.ts";
import { toast } from "vue-sonner";
import { Separator } from "@/components/ui/separator";

const router = useRouter();
const defaultPlaceholder = today(getLocalTimeZone())
const date = ref() as Ref<DateValue>
const df = new DateFormatter('en-UK', {
  dateStyle: 'long',
})

const vehicles: Ref<any[] | null> = ref(null)
const registration: Ref<string | number | undefined> = ref(undefined)
const litres: Ref<string | number | undefined> = ref(undefined)
const miles: Ref<string | number | undefined> = ref(undefined)
const price_per_litre: Ref<string | number | undefined> = ref(undefined)
const total_cost: Ref<string | number | undefined> = ref(undefined)
const mpg: Ref<number | undefined> = ref(undefined)

onMounted(() => {
  // Get list of vehicles registered to the user
  callAPI('/api/v1/vehicles', 'GET')
      .then((json) => {
        vehicles.value = json
      }).catch((err) => {
    toast.error('Failure', {description: err.toString()})
  })
})

const priceModel = computed({
  get: () => price_per_litre.value,
  set: (val: number | null) => {
    price_per_litre.value = val === null ? undefined : val

    if (litres.value && val != null && typeof litres.value === "number") {
      total_cost.value = +(litres.value * (val / 100)).toFixed(2)
    } else {
      total_cost.value = undefined
    }
  }
})

const totalModel = computed({
  get: () => total_cost.value,
  set: (val: number | null) => {
    total_cost.value = val === null ? undefined : val

    if (litres.value && val != null && typeof litres.value === "number") {
      price_per_litre.value = +((val * 100) / litres.value).toFixed(1)
    } else {
      price_per_litre.value = undefined
    }
  }
})

watch([total_cost, price_per_litre, litres, miles], () => {
  if (typeof litres.value != 'number' || typeof miles.value != 'number') {
    return
  }

  const gallons: number = litres.value / 4.546;
  mpg.value = Math.round((miles.value / gallons) * 1e2) / 1e2;
})


const submit = () => {
  if (
      typeof litres.value != 'number' ||
      typeof miles.value != 'number' ||
      typeof total_cost.value != 'number' ||
      typeof mpg.value != 'number' ||
      typeof date.value == 'undefined' ||
      typeof registration.value != 'string'
  ) {
    toast.warning('Warning', {description: "Cannot submit with missing fields."})
    return
  }

  const payload = {
    registration: registration.value,
    date: date.value.toString(),
    litres: litres.value,
    miles: miles.value,
    mpg: mpg.value,
    total_cost: total_cost.value
  }

  callAPI('/api/v1/mpg', 'POST', payload)
    .then((data) => {
      console.log(data)
      toast.success('Refuel log successfully submitted.')
      sleep(2)
      movePage(router, '/')
    }).catch((error) => {
      console.error(error)
      toast.error(error.toString())
    })
}

document.title = 'MPG Service | Log a refuel'
</script>

<template>
  <main>
    <div class="flex flex-col justify-center items-center xl:mt-12 pb-40">
      <div class="mt-8 w-[95%] xl:w-full flex justify-center flex-col text-center items-center">
        <Card class="w-full max-w-sm mt-4">
          <CardHeader>
            <CardTitle>Log a refuel</CardTitle>
            <CardDescription>
              Enter the amount of litres used, miles driven & the cost to fill up below.
            </CardDescription>
          </CardHeader>
          <Separator class="mb-2" />
          <CardContent>
            <form>
              <div class="grid grid-cols-1 w-full items-center gap-4">
                <div class="flex flex-col space-y-1.5 items-center">
                  <div class="flex flex-col space-y-1.5 items-center mb-6">
                    <Label>Date</Label>
                    <Popover v-slot="{ close }">
                      <PopoverTrigger as-child>
                        <Button
                            variant="outline"
                            :class="cn('w-60 justify-start text-left font-normal', !date && 'text-muted-foreground')"
                        >
                          <CalendarIcon />
                          {{ date ? df.format(date.toDate(getLocalTimeZone())) : "Pick a date" }}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent class="w-auto p-0" align="start">
                        <Calendar
                            v-model="date"
                            :default-placeholder="defaultPlaceholder"
                            layout="month-and-year"
                            initial-focus
                            @update:model-value="close"
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                  <Label>Vehicle</Label>
                  <Select v-model="registration">
                    <SelectTrigger>
                      <SelectValue placeholder="Select Vehicle" />
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
                </div>
                <Separator class="my-4" />
                <div class="flex flex-row space-y-1.5 space-x-5">
                  <div class="flex flex-col space-y-1.5">
                    <Label for="litres">Litres</Label>
                    <Input id="litres" type="number" placeholder="45.21" required v-model="litres" />
                  </div>
                  <div class="flex flex-col space-y-1.5">
                    <Label for="miles">Miles</Label>
                    <Input id="miles" type="number" placeholder="324.6" required v-model="miles" />
                  </div>
                </div>
                <div class="flex flex-row space-y-1.5 space-x-5">
                  <div class="flex flex-col space-y-1.5">
                    <Label for="ppl">Price per Litre</Label>
                    <Input id="ppl" type="number" placeholder="136.9" v-model="priceModel" />
                  </div>

                  <div class="flex flex-col space-y-1.5">
                    <Label for="cost">Total Cost</Label>
                    <Input id="cost" type="number" placeholder="56.20" v-model="totalModel" />
                  </div>
                </div>
              </div>
            </form>
          </CardContent>
          <CardFooter class="mt-2 grid grid-cols-2 gap-2">
            <div class="bg-accent p-1.5 rounded-md flex flex-cols-2 gap-1 w-full justify-center dark:brightness-75 hover:cursor-not-allowed">
              <p>{{ mpg ? mpg : 0 }}</p>
              <p>mi/G</p>
            </div>
            <Button class="w-full hover:cursor-pointer" @click.prevent="submit()">
              Submit
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  </main>
</template>
