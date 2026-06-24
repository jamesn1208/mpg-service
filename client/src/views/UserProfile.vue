<script setup lang="ts">
import PageBreak from "@/components/PageBreak.vue";
import { Icon } from '@iconify/vue';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { toast } from 'vue-sonner';
import { useRouter } from "vue-router";
import {
  ref,
  type Ref,
  onMounted,
} from "vue";
import {
  callAPI,
  movePage
} from "@/lib/common.ts";
import {
  Dialog, DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { useAuthStore } from '@/stores/auth.ts'
import EditVehicleForm from "@/components/EditVehicleForm.vue";

const router = useRouter();
const auth = useAuthStore();
const username_editable: Ref<boolean> = ref(false);
const password_editable: Ref<boolean> = ref(false);
const password: Ref<string | number | undefined> = ref(undefined);
const username: Ref<string | number | undefined> = ref(undefined);
const user: Ref<{id: number, username: string} | undefined> = ref(undefined);
const vehicles: Ref<[{registration: string, make: string, emissions: number, year: number, colour: string}] | undefined> = ref(undefined);

onMounted(() => {
  if (!auth.isLoggedIn) {
    return
  }

  callAPI('/api/v1/vehicles', 'GET')
    .then((json) => {
      vehicles.value = json;
    })
    .catch((error) => {
      toast.error('Error', {description: error.message});
    })

  callAPI('/api/v1/users', 'GET')
    .then((json) => {
      user.value = json;
      username.value = json.username;
    }).catch((error) => {
      toast.error('Error', {description: error.message});
  })
})

const deleteAccount = () => {
  callAPI('/api/v1/users', 'DELETE')
      .then((json) => {
        toast.success('Success', {description: json.message});
      }).catch((error) => {
    toast.error('Error', {description: error.toString});
  })

  auth.logout()
  movePage(router, '/')
}

const saveProfile = () => {
  if (typeof user.value == 'undefined' || username.value === user.value.username && typeof password.value == 'undefined' || typeof username.value == 'undefined') {
    toast.warning('Warning', {description: "Nothing to save!"});
    return
  }

  const payload: { username?: string; password?: string } = {}

  if (username.value !== user.value.username) {
    payload.username = username.value.toString()
  }
  if (typeof password.value !== 'undefined') {
    payload.password = password.value.toString()
  }

  if (!payload.password && !payload.username) {
    toast.warning('Warning', {description: "Nothing to save!"});
    return
  }

  callAPI('/api/v1/users', 'PATCH', payload)
    .then((json) => {
      toast.success('Success', {description: json.message});
    }).catch((error) => {
      toast.error('Error', {description: error.toString});
  })
}

document.title = 'MPG Service | User Profile'
</script>

<template>
  <main class="pb-30">
    <div class="flex flex-col items-center justify-center mt-6">
      <h2 class="text-3xl font-bold mb-4">Profile</h2>
      <PageBreak/>
      <div class="mt-8 flex flex-col justify-center items-center">
        <div v-if="!auth.isLoggedIn" class="flex flex-cols-2 gap-2 mt-2">
          <Icon icon="material-symbols:warning-rounded" class="scale-120 brightness-75" />
          <h2 class="brightness-75">You are not logged in.</h2>
        </div>
        <div class="flex flex-col justify-center items-center px-6 py-4 bg-primary-foreground rounded-lg w-[90%] xl:w-fit" v-if="auth.isLoggedIn">
          <h3 class="text-xl">Your account</h3>

          <PageBreak class="mt-4 mb-4"/>

          <Label for="username">Username</Label>
          <div class="flex flex-cols-2 items-center mt-2 gap-3">
            <Input
                class="h-full align-middle text-xl border-2 rounded-lg px-4 py-2"
                id="username"
                :disabled="!username_editable"
                v-model="username"
            />
            <Button
                class="hover:cursor-pointer"
                @click.prevent="() => username_editable = !username_editable"
            >
              <Icon icon="mdi:pencil-outline" class="scale-160"/>
            </Button>
          </div>

          <span class="mt-6" />

          <Label for="password">Password</Label>
          <div class="flex flex-cols-2 items-center mt-2 gap-3">
            <Input
                class="h-full align-middle text-xl border-2 rounded-lg px-4 py-2"
                id="password"
                placeholder="********"
                v-model="password"
                :disabled="!password_editable"/>
            <Button
                class="hover:cursor-pointer"
                @click.prevent="() => password_editable = !password_editable"
            >
              <Icon icon="mdi:pencil-outline" class="scale-160"/>
            </Button>
          </div>

          <div class="grid grid-cols-2 items-center mt-2 gap-3 w-full">
            <Button
                class="hover:cursor-pointer w-full mt-6"
                @click.prevent="saveProfile()"
            >
              Save
            </Button>
            <Dialog>
              <DialogTrigger><Button
                  class="hover:cursor-pointer w-full mt-6"
                  variant="destructive"
                  @click.prevent=""
              >
                Delete Account
              </Button></DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Are you absolutely sure?</DialogTitle>
                  <DialogDescription>
                    This action cannot be undone. This will permanently delete your account
                    and remove your data from our servers.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter class="gap-2 xl:gap-4 mt-4">
                  <Button variant="destructive" class="hover:cursor-pointer" @click.prevent="deleteAccount()">Yes, delete my account</Button>
                  <DialogClose as-child>
                    <Button class="hover:cursor-pointer">No, keep my account</Button>
                  </DialogClose>
                </DialogFooter>
              </DialogContent>
            </Dialog>

          </div>
        </div>
      </div>
      <PageBreak class="my-10"/>

      <div class="w-[90%] flex flex-col items-center justify-center xl:w-[75%]">
        <h3 class="text-2xl">Your vehicles</h3>
        <div v-if="!vehicles" class="w-[90%] mt-6 inline-flex gap-2 items-center outline-destructive outline-2 outline-dashed p-2 rounded-xl lg:w-fit">
          <Icon icon="material-symbols:warning-rounded" class="scale-200 lg:scale-125 mx-2 lg:mr-0"/>
          <p class="brightness-75">You have not registered any vehicles yet!</p>
        </div>
        <div class="w-full grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 items-center justify-center gap-14 mt-6" v-if="vehicles">
          <div class="bg-primary-foreground rounded-xl p-6 w-full" v-for="vehicle in vehicles">
            <div class="w-full text-center mb-4">
              <h3 class="text-xl font-light">{{ vehicle.registration }}</h3>
            </div>
            <PageBreak class="my-3"/>
            <div class="grid grid-cols-2 gap-4">
              <div class="grid grid-cols-1 w-full p-4 bg-violet-200 dark:bg-violet-500 rounded-3xl text-center">
                <h4 class="font-bold">Year</h4>
                <p>{{ vehicle.year }}</p>
              </div>
              <div class="grid grid-cols-1 w-full p-4 bg-violet-200 dark:bg-violet-500 rounded-3xl text-center">
                <h4 class="font-bold">Colour</h4>
                <p>{{ vehicle.colour }}</p>
              </div>
              <div class="grid grid-cols-1 w-full p-4 bg-violet-200 dark:bg-violet-500 rounded-3xl text-center">
                <h4 class="font-bold">Emissions</h4>
                <p>{{ vehicle.emissions }}g/km</p>
              </div>
              <div class="grid grid-cols-1 w-full p-4 bg-violet-200 dark:bg-violet-500 rounded-3xl text-center">
                <h4 class="font-bold">Make</h4>
                <p>{{ vehicle.make }}</p>
              </div>
            </div>
            <PageBreak class="my-3"/>
            <div class="flex flex-cols-2 gap-2 mt-4 justify-items-center justify-end">
              <EditVehicleForm
                :year="vehicle.year"
                :colour="vehicle.colour"
                :make="vehicle.make"
                :registration="vehicle.registration"
                :emissions="vehicle.emissions"
              />
              <Button variant="destructive" class="hover:cursor-pointer w-24">
                <Icon icon="fa7-solid:chain-broken"/>
                Unlink
              </Button>
            </div>
          </div>
        </div>
      </div>

      <Button class="hover:cursor-pointer mt-8" @click.prevent="() => movePage(router, '/new-vehicle')">Add a new vehicle</Button>
    </div>
  </main>
</template>
