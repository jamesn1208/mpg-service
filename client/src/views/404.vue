<script setup lang="ts">
document.title = 'MPG Service | Not Found'
</script>

<template>
<div class="flex items-center justify-center">
  <div class="flex flex-col items-center justify-center gap-6 py-12">
    <h1><font-awesome-icon icon="fa-solid fa-hurricane" class="animate-spin"/> 404</h1>

    <p class="opacity-80 text-base">The page that you are looking for does not exist.</p>

    <div class="hover:scale-110 hover:animate-wiggle duration-200 ease-in-out flex items-center gap-2 text-lg">
      <font-awesome-icon icon="fa-solid fa-chevron-left" class="text-2xl"/>
      <a class="underline" href="/">
        Go back to safety!
      </a>
    </div>
  </div>
</div>
</template>

<style scoped>
  h1 {
    font-size: 6rem;
    font-weight: bold;
  }
</style>
