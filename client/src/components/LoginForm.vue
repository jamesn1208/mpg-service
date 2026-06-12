<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
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
  fetch('http://localhost:3333/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: (e.target as HTMLFormElement).email.value,
      password: (e.target as HTMLFormElement).password.value,
    }),
  })
      .then(res => res.json())
      .then(data => {
        if (data.error_message) {
          throw new Error(data.error_message)
        }

        localStorage.setItem('user_id', data.user_id)
        toast('Success', { description: 'Logged in' })
      })
      .then(() => new Promise(f => setTimeout(f, 1000)))
      .then(() => router.push('/').then(() => {window.location.reload()}))
      .catch(reason => {
        console.error(reason)
        toast('Failure', { description: reason.toString() })
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
          Enter your email below to login to your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field>
              <FieldLabel for="email">
                Email
              </FieldLabel>
              <Input
                id="email"
                type="email"
                placeholder="mail@example.com"
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
