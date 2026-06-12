<script setup lang="ts">
import { Separator } from '@/components/ui/separator'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import {Card, CardDescription, CardFooter, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {toast} from "vue-sonner";
import {useRoute, useRouter} from "vue-router";
import {ref} from 'vue';
import {Spinner} from "@/components/ui/spinner";

const route = useRoute()
const router = useRouter()
const userProfile = ref()

function movePage(s: string) {
  router.push(s)
}

fetch(`http://localhost:3333/users/${route.params.id}`, {
  method: 'GET',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})
    .then(res => res.json())
    .then(data => {
      if (data.error_message) {
        throw new Error(data.error_message)
      }

      console.log(data);
      userProfile.value = data;
    })
    .catch(reason => {
      console.error(reason)
      toast('Failure', { description: reason.toString() })
    })


document.title = 'MPG Service | User Profile'
</script>

<template>
  <main>
    <div class="w-full flex flex-col items-center pb-10">
      <Spinner v-if="!userProfile" class="stroke-3 size-6 mt-6"/>
      <div v-if="userProfile" class="w-1/2 flex flex-col items-center mt-8 gap-12">
        <h1 class="text-2xl font-bold">{{ userProfile.first_name + ' ' + userProfile.last_name}}</h1>

        <p class="text-muted-foreground">Notice: Due to GDPR concerns, we no longer share user's email addresses.</p>

        <Separator/>

        <Accordion type="single" collapsible class="w-9/10" default-value="listed">
          <AccordionItem value="listed">
            <AccordionTrigger>Listed Items</AccordionTrigger>
            <AccordionContent>
              <div class="mt-4 mb-4 flex gap-x-6 gap-y-8 flex-wrap max-w-full justify-center">
                <Card class="w-50 max-h-60 text-center" v-for="(data, i) in userProfile.selling" :key="i">
                  <CardHeader>
                    <CardTitle>{{ data.name }}</CardTitle> <!-- TODO: Fix this element -->
                    <CardDescription class="truncate max-h-10">
                      {{ data.description }}
                    </CardDescription> <!-- TODO: Fix this element -->
                  </CardHeader>
                  <CardFooter>
                    <Button variant="outline" class="w-full hover:cursor-pointer" type="button" @click="movePage(`/items/${data.item_id}`)">
                      View Item
                    </Button> <!-- TODO: Fix the @click element -->
                  </CardFooter>
                </Card>
                <p v-if="userProfile.selling.length === 0" class="text-muted-foreground">This user is currently not selling anything.</p>
              </div>
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="bidding">
            <AccordionTrigger>Bidding On</AccordionTrigger>
            <AccordionContent>
              <div class="mt-4 mb-4 flex gap-x-6 gap-y-8 flex-wrap max-w-full justify-center">
                <Card class="w-50 max-h-60 text-center" v-for="(data, i) in userProfile.bidding_on" :key="i">
                  <CardHeader>
                    <CardTitle>{{ data.name }}</CardTitle>
                    <CardDescription class="truncate max-h-10">
                      {{ data.description }}
                    </CardDescription>
                  </CardHeader>
                  <CardFooter>
                    <Button variant="outline" class="w-full hover:cursor-pointer" type="button" @click="movePage(`/items/${data.item_id}`)">
                      View Item
                    </Button>
                  </CardFooter>
                </Card>
                <p v-if="userProfile.bidding_on.length === 0" class="text-muted-foreground">This user is currently not bidding on anything.</p>
              </div>
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="bought">
            <AccordionTrigger>Items Bought</AccordionTrigger>
            <AccordionContent>
              <div class="mt-4 mb-4 flex gap-x-6 gap-y-8 flex-wrap max-w-full justify-center">
                <Card class="w-50 max-h-60 text-center" v-for="(data, i) in userProfile.auctions_ended" :key="i">
                  <CardHeader>
                    <CardTitle>{{ data.name }}</CardTitle>
                    <CardDescription class="truncate max-h-10">
                      {{ data.description }}
                    </CardDescription>
                  </CardHeader>
                  <CardFooter>
                    <Button variant="outline" class="w-full hover:cursor-pointer" type="button" @click="movePage(`/items/${data.item_id}`)">
                      View Item
                    </Button>
                  </CardFooter>
                </Card>
                <p v-if="userProfile.auctions_ended.length === 0" class="text-muted-foreground">This user has never bought anything from here.</p>
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
    </div>
  </main>
</template>
