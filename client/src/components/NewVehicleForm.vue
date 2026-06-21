<script setup lang="ts">
import {
  type HTMLAttributes,
  ref,
  type Ref
} from "vue"
import { cn } from "@/lib/utils"
import {
  callAPI,
  movePage,
  sleep
} from "@/lib/common"
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  Field,
  FieldGroup,
  FieldLabel,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'
import { Icon } from '@iconify/vue';


const router = useRouter()
const data: Ref = ref(undefined)

const registration: Ref<string | number | undefined> = ref(undefined)
const make: Ref<string | number | undefined> = ref(undefined)
const colour: Ref<string | number | undefined> = ref(undefined)
const emissions: Ref<string | number | undefined> = ref(undefined)
const year: Ref<string | number | undefined> = ref(undefined)


const getVehicleData = () => {
  if (typeof registration.value != 'string' || registration.value.length <= 0 || registration.value.length > 7) {
    toast.warning('Warning', {description: "You must enter a valid registration number."})
    return
  }

  callAPI(`/api/v1/vehicles/lookup/${registration.value}`, 'GET')
    .then((json) => {
      data.value = json
      make.value = json.make
      colour.value = json.colour
      year.value = json.year
      emissions.value = json.emissions
    }).catch((error) => {
      toast.error('Error', {description: error.toString()})
    })
}

function handleSubmit() {
  if (
      typeof registration.value != 'string' ||
      typeof make.value != 'string' ||
      typeof emissions.value != 'number' ||
      typeof year.value != 'number' ||
      typeof colour.value != 'string'
  ) {
    toast.warning('Warning', {description: "You must enter valid vehicle information."})
    return
  }

  const payload = {
    registration: registration.value,
    make: make.value,
    year: year.value,
    emissions: emissions.value,
    colour: colour.value
  }

  callAPI('/api/v1/vehicles', 'POST', payload)
    .then(async (json) => {
      toast.success('Success', {description: json.message})
      await sleep(2)
      movePage(router, '/profile')
    }).catch((error) => {
      toast.error('Error', {description: error.toString()})
  })
}

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()
</script>

<template>
  <div :class="cn('flex flex-col gap-6', props.class)">
    <Card>
      <CardHeader class="text-center">
        <div class="inline-flex gap-2 text-center w-full justify-center">
          <Icon icon="fa-solid:car"/>
          <CardTitle>Add a new vehicle</CardTitle>
        </div>
        <CardDescription>
          Add a new vehicle using it's registration. Information will be auto-filled from the DVLA database.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field class="mb-2 gap-2">
              <FieldLabel for="registration">
                Registration
              </FieldLabel>
              <Input
                  id="registration"
                  type="text"
                  v-model="registration"
                  placeholder="Registration"
                  required
              />
              <Button @click.prevent="getVehicleData()" type="button" :disabled="data" class="hover:cursor-pointer"><Icon icon="material-symbols:search"/>Lookup</Button>
            </Field>
            <div v-if="data">
              <Field class="mb-2 gap-2">
                <div class="flex items-center">
                  <FieldLabel for="make">
                    Make
                  </FieldLabel>
                </div>
                <Input
                    id="make"
                    type="text"
                    v-model="make"
                    required
                />
              </Field>
              <Field class="mb-2 gap-2">
                <div class="flex items-center">
                  <FieldLabel for="colour">
                    Colour
                  </FieldLabel>
                </div>
                <Input
                    id="colour"
                    type="text"
                    v-model="colour"
                    required
                />
              </Field>
              <Field class="mb-2 gap-2">
                <div class="flex items-center">
                  <FieldLabel for="year">
                    Year
                  </FieldLabel>
                </div>
                <Input
                    id="year"
                    type="number"
                    v-model="year"
                    required
                />
              </Field>
              <Field class="mb-2 gap-2">
                <div class="flex items-center">
                  <FieldLabel for="emissions">
                    Emissions (g/km)
                  </FieldLabel>
                </div>
                <Input
                    id="emissions"
                    type="number"
                    v-model="emissions"
                    required
                />
              </Field>
              <Field class="mt-6">
                <Button type="submit" class="hover:cursor-pointer">
                  Add
                </Button>
                <Button class="hover:cursor-pointer" variant="secondary" @click.prevent="() => movePage(router, '/profile')">Cancel</Button>
              </Field>
            </div>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
