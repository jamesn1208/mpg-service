<script setup lang="ts">
import {
  type HTMLAttributes,
  ref,
  type Ref
} from "vue"
import { cn } from "@/lib/utils"
import {
  callAPI,
  sleep,
  movePage,
  getFakeUsername
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
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from '@/components/ui/field'
import { Input } from '@/components/ui/input'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'
import { useAuthStore } from '@/stores/auth'


const router = useRouter()
const auth = useAuthStore()
const username: Ref<string | number | undefined> = ref(undefined)
const password: Ref<string | number | undefined> = ref(undefined)


const handleSubmit = () => {
  if (typeof username.value != "string" || typeof password.value != "string") {
    toast.info('Information', {description: "You must fill in the username & password fields to login."})
    return
  }

  callAPI(
      '/api/v1/users/login',
      'POST',
      {
        username: username.value as string,
        password: password.value as string,
      }
  ).then((data) => {
    toast('Success', { description: 'Logged in' })
    auth.login(data.id)
    sleep(2)
    movePage(router, '/')
  }).catch((e) => {
    toast.error('Failure', {description: e.toString()})
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
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>
          Enter your username below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field>
              <FieldLabel for="username">
                Username
              </FieldLabel>
              <Input
                id="username"
                type="text"
                v-model="username"
                :placeholder="getFakeUsername()"
                required
              />
            </Field>
            <Field>
              <div class="flex items-center">
                <FieldLabel for="password">
                  Password
                </FieldLabel>
              </div>
              <Input
                  id="password"
                  type="password"
                  v-model="password"
                  required
              />
            </Field>
            <Field>
              <Button type="submit" class="hover:cursor-pointer">
                Login
              </Button>
              <FieldDescription class="text-center">
                Don't have an account?
                <RouterLink to="/sign-up">
                  Sign up
                </RouterLink>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
