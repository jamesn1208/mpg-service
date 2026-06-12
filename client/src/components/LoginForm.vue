<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { callAPI, movePage, sleep } from "@/lib/common"
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


const router = useRouter()


const handleSubmit = (e: Event) => {
  let data

  try {
    data = callAPI(
        '/api/v1/users/login',
        'POST',
        {
          username: (e.target as HTMLFormElement).username.value,
          password: (e.target as HTMLFormElement).password.value,
        }
    )
  } catch (e) {
    toast.error('Failure', {description: e as string})
    return
  }

  toast('Success', { description: 'Logged in' })
  localStorage.setItem('user_id', data.id)

  sleep(2)
  movePage(router, '/')
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
                placeholder="billy_bob13"
                required
              />
            </Field>
            <Field>
              <div class="flex items-center">
                <FieldLabel for="password">
                  Password
                </FieldLabel>
              </div>
              <Input id="password" type="password" required />
            </Field>
            <Field>
              <Button type="submit" class="hover:cursor-pointer">
                Login
              </Button>
              <FieldDescription class="text-center">
                Don't have an account?
                <a href="/sign-up">
                  Sign up
                </a>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
