<script setup lang="ts">
import type { HTMLAttributes } from "vue"
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

const router = useRouter()

const handleSubmit = (e: Event) => {
  let name_array = (e.target as HTMLFormElement).name.value.split(' ')
  const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$#!%*?&]{8,}$/
  if (!password_regex.test((e.target as HTMLFormElement).password.value)) {
    toast('Failure', { description: 'Password does not meet complexity requirements.' })
    return
  }
  if (name_array.length < 2) {
    toast('Failure', { description: 'Please enter both a first and last name.' })
    return
  }

  fetch('http://localhost:3333/users', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      first_name: name_array[0],
      last_name: name_array[name_array.length - 1],
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
        toast('Success', { description: 'Account created.' })
      })
      .then(() => new Promise(f => setTimeout(f, 1000)))
      .then(() => router.push('/'))
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
        <CardTitle class="text-xl">
          Create your account
        </CardTitle>
        <CardDescription>
          Enter your email below to create your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="handleSubmit">
          <FieldGroup>
            <Field>
              <FieldLabel for="name">
                Full Name
              </FieldLabel>
              <Input id="name" type="text" placeholder="John Doe" required />
            </Field>
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
                Already have an account? <a href="/login">Sign in</a>
              </FieldDescription>
            </Field>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
