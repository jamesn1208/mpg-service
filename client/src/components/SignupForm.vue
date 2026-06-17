<script setup lang="ts">
import {
  type HTMLAttributes,
  ref,
  type Ref
} from "vue"
import { cn } from '@/lib/utils'
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
import {
  callAPI,
  getFakeUsername,
  movePage,
  sleep
} from "@/lib/common.ts";
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username: Ref<string | number | undefined> = ref(undefined)
const password: Ref<string | number | undefined> = ref(undefined)


const handleSubmit = () => {
  if (typeof username.value != "string" || typeof password.value != "string") {
    toast.info('Information', {description: "You must fill in the username & password fields to create your account."})
    return
  }

  const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$#!%*?&]{8,}$/
  if (!password_regex.test(password.value)) {
    toast('Failure', { description: 'Password does not meet complexity requirements.' })
    return
  }

  callAPI(
      '/api/v1/users',
      'POST',
      {
        username: username.value,
        password: password.value,
      }
  ).then((data) => {
    toast('Success', { description: 'Account created.' })
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
        <CardTitle class="text-xl">
          Create your account
        </CardTitle>
        <CardDescription>
          Enter a username below to create your account
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
                :placeholder="getFakeUsername()"
                required
              />
            </Field>
            <Field>
              <Field class="mb-2">
                <FieldLabel for="password">
                  Password
                </FieldLabel>
                <Input id="password" type="password" required />
              </Field>
              <FieldDescription>
                Must be at least 8 characters long.<br>
                Must contain at least:<br>
                  - One uppercase letter<br>
                  - One lowercase letter<br>
                  - One number<br>
                  - One special character (e.g. %, #, $, !)<br>
              </FieldDescription>
            </Field>
            <Field>
              <Button type="submit" class="hover:cursor-pointer">
                Create Account
              </Button>
              <FieldDescription class="text-center">
                Already have an account?
              <RouterLink to="/login">
                Login
              </RouterLink>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
