<script setup lang="ts">
import { Separator } from '@/components/ui/separator'
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useRouter } from 'vue-router'
import { Clock } from 'lucide-vue-next'
import {toast} from "vue-sonner";
import {ref} from "vue";
const router = useRouter()
const pageData = ref()

function movePage(s: string) {
  router.push(s)
}

const populate = () => {
    fetch('http://localhost:3333/search?limit=30', {
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
          let formattedData = [];

          // Remove expired auctions from homepage (users don't care about things they cant buy)
          for (let i = 0; i < data.length; i++) {
            if (data[i].end_date > new Date()) {
              formattedData.push(data[i]);
            }
          }
          pageData.value = formattedData;
        })
        .catch(reason => {
          console.error(reason)
          toast('Failure', {description: reason.toString()})
        })
  }
populate()

document.title = 'MPG Service | Home'
</script>

<template>
  <main>
    <div class="w-full pb-10">
      <div class="w-full flex justify-center items-center flex-col">
<!--        <img src="../assets/sale.svg" alt="Home page sale banner" class="w-8/9 dark:invert-90" />-->
        <p class="text-sm italic text-gray-400 dark:text-gray-600">*Only applies to participating auctions</p>
      </div>
      <Separator class="my-6" />
      <div class="w-full flex flex-col items-center">
        <div class="inline-flex items-center gap-2">
          <Clock class="stroke-3 dark:stroke-yellow-200"/>
          <h2 class="text-2xl font-bold">Recent Auctions</h2>
          <Clock class="stroke-3 dark:stroke-yellow-200"/>
        </div>
        <p class="mb-10 mt-1 text-muted-foreground italic">These items were listed recently.</p>
        <div class="flex gap-8 flex-wrap max-w-full justify-center">
          <Card class="w-50 max-h-60 text-center" v-for="(data, i) in pageData" :key="i">
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
          <p v-if="!pageData || pageData.length === 0" class="text-muted-foreground">No auctions found, try again later.</p>
        </div>
      </div>
    </div>
  </main>
</template>
