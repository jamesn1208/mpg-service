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

const router = useRouter();
const auth = useAuthStore();
const username_editable: Ref<boolean> = ref(false);
const password_editable: Ref<boolean> = ref(false);
const password: Ref<string | number | undefined> = ref(undefined);
const username: Ref<string | number | undefined> = ref(undefined);
const data: Ref<any> = ref(undefined);

onMounted(() => {
  callAPI('/api/v1/users', 'GET')
    .then((json) => {
      data.value = json;
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
  if (username.value === data.value.username && typeof password.value == 'undefined' || typeof username.value == 'undefined') {
    toast.warning('Warning', {description: "Nothing to save!"});
    return
  }

  const payload: { username?: string; password?: string } = {}

  if (username.value !== data.value.username) {
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
  <main>
    <div class="flex flex-col items-center justify-center mt-6">
      <h2 class="text-3xl font-bold mb-4">Profile</h2>
      <PageBreak/>
      <div class="mt-8">
        <div class="flex flex-col justify-center items-center px-6 py-4 bg-primary-foreground rounded-lg">
          <h3 class="text-xl">Your account</h3>

          <PageBreak class="mt-4 mb-4"/>

          <Label for="username">Username</Label>
          <div class="flex flex-cols-2 items-center mt-2 gap-3">
            <Input
                class="h-full align-middle text-xl border-2 rounded-xl px-4 py-2"
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
                class="h-full align-middle text-xl border-2 rounded-xl px-4 py-2"
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
                <DialogFooter class="gap-4">
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
    </div>
  </main>
<!--Show all vehicles registered to the user-->
<!--Ability to add a new vehicle-->
</template>
