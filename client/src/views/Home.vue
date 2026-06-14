<script setup lang="ts">
import PageBreak from "@/components/PageBreak.vue";

document.title = 'MPG Service | Home'

// Hard set data to show what the page should look like eventually
const data: any[] = [
  {
    title: "Most Driven Vehicle",
    value: "WA67 USH",
  },
  {
    title: "CO² Released",
    value: "1260.6 KG",
  },
  {
    title: "Total Spent",
    value: "£2614.23",
  },
  {
    title: "Total Miles",
    value: "9521.28 mi",
  },
  {
    title: "Lowest p/L",
    value: "116.7p",
  },
  {
    title: "Highest p/L",
    value: "162.9p",
  },
  {
    title: "Number Of Refuels",
    value: "28",
  },
  {
    title: "Average £/mi",
    value: "£0.21",
  },
  {
    title: "Average p/L",
    value: "132.4p",
  },
  {
    title: "Lowest MPG",
    value: "27.21 mi/G",
  },
  {
    title: "Average MPG",
    value: "35.62 mi/G",
  },
  {
    title: "Highest MPG",
    value: "48.20 mi/G",
  },
]


</script>

<template>
  <main>
    <div class="w-full pb-20">
      <div class="w-full flex justify-center items-center mt-12 mb-12">
        <img
          alt="Website logo"
          class="h-5/6 w-5/6 lg:h-1/2 lg:w-1/2 xl:h-1/3 xl:w-1/3"
          src="../assets/logo.svg"
        />
      </div>
      <PageBreak />
      <h2 class="text-5xl mt-8 mb-4 w-full text-center">Statistics</h2>
      <div class="w-full flex justify-center">
        <div class="grid grid-cols-1 gap-8 lg:grid-cols-2 lg:gap-8 xl:grid-cols-3 xl:gap-10 mt-4 place-items-center w-full">
          <div
              class="p-4 w-[90%] h-fit lg:min-w-md lg:min-h-60 rounded-3xl bg-secondary grid grid-cols-1 gap-4 text-center"
              v-for="d in data"
              :key="d.title">
            <h3 class="text-2xl lg:text-3xl font-extralight">{{ d.title }}</h3>  <!-- Title -->
            <div class="flex w-full justify-center">  <!-- Value -->
              <p class="py-4 px-10 text-4xl lg:text-7xl font-bold rounded-full bg-card w-fit h-fit">{{ d.value }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
