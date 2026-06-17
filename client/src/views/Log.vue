<script setup lang="ts">
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
  type Ref
} from 'vue'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { callAPI } from "@/lib/common.ts";
import { toast } from "vue-sonner";
import { Separator } from "@/components/ui/separator";

const vehicles: Ref<any[] | null> = ref(null)
const registration: Ref<string | number | undefined> = ref(undefined)
const litres: Ref<string | number | undefined> = ref(undefined)
const miles: Ref<string | number | undefined> = ref(undefined)
const price_per_litre: Ref<string | number | undefined> = ref(undefined)
const total_cost: Ref<string | number | undefined> = ref(undefined)

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

document.title = 'MPG Service | Log a refuel'
</script>

<template>
  <main>
    <div class="flex flex-col justify-center items-center xl:mt-12 pb-30">
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
          <CardFooter class="mt-2 flex flex-col gap-2">
            <Button class="w-full">
              Submit
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  </main>
</template>
