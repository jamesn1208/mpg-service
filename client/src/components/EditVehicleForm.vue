<script setup lang="ts">
import {
  type HTMLAttributes,
  ref,
  type Ref
} from "vue"
import { cn } from "@/lib/utils"
import {
  callAPI,
  sleep
} from "@/lib/common"
import {
  Field,
  FieldGroup,
  FieldLabel,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { toast } from 'vue-sonner'
import {
  Dialog, DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle, DialogTrigger
} from "@/components/ui/dialog";
import {Icon} from "@iconify/vue";
import {Button} from "@/components/ui/button";


function handleSubmit() {
  if (
      typeof make.value != 'string' ||
      typeof emissions.value != 'number' ||
      typeof year.value != 'number' ||
      typeof colour.value != 'string'
  ) {
    toast.warning('Warning', {description: "You must enter valid vehicle information."})
    return
  }

  const payload: {make?: string, emissions?: number, year?: number, colour?: string} = {}

  if (make.value !== props.make) {
    payload.make = make.value
  }
  if (colour.value !== props.colour) {
    payload.colour = colour.value
  }
  if (year.value !== props.year) {
    payload.year = year.value
  }
  if (emissions.value !== props.emissions) {
    payload.emissions = emissions.value
  }

  if (Object.keys(payload).length === 0) {
    toast.warning('Warning', {description: "You haven't changed any fields."})
    return
  }

  callAPI(`/api/v1/vehicles/${registration.value}`, 'PATCH', payload)
    .then(async (json) => {
      toast.success('Success', {description: json.message})
      await sleep(2)
      window.location.reload()
    }).catch((error) => {
    toast.error('Error', {description: error.toString()})
  })
}

const props = defineProps<{
  class?: HTMLAttributes["class"],
  make: string,
  year: number,
  registration: string,
  emissions: number,
  colour: string
}>()

const registration: Ref<string | number | undefined> = ref(props.registration)
const make: Ref<string | number | undefined> = ref(props.make)
const colour: Ref<string | number | undefined> = ref(props.colour)
const emissions: Ref<string | number | undefined> = ref(props.emissions)
const year: Ref<string | number | undefined> = ref(props.year)
</script>

<template>
  <div :class="cn('flex flex-col gap-6', props.class)">
    <Dialog>
      <DialogTrigger><Button
          class="hover:cursor-pointer w-24"
          @click.prevent=""
      >
        <Icon icon='mdi:pencil-outline'/>Edit
      </Button></DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit vehicle | {{ registration }}</DialogTitle>
          <DialogDescription>
            This allows you to update information about your vehicle. This cannot be rolled back, so make sure it's accurate!
          </DialogDescription>
        </DialogHeader>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field class="gap-2 mt-4">
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
            <Field class="gap-2">
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
            <Field class="gap-2">
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
            <Field class="gap-2 mb-4">
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
          </FieldGroup>
        </form>
        <DialogFooter class="gap-2 xl:gap-4 mt-4">
          <Button class="hover:cursor-pointer" @click="handleSubmit">Save</Button>
          <DialogClose as-child>
            <Button class="hover:cursor-pointer" variant="secondary">Cancel</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
