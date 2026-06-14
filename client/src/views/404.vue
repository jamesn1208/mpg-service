<script setup lang="ts">
document.title = 'MPG Service | Not Found'
</script>

<template>
<div class="flex items-center justify-center">
  <div class="flex flex-col items-center justify-center gap-6 py-12">
    <h1 class="text-9xl font-bold">
      <font-awesome-icon icon="fa-solid fa-hurricane" class="animate-spin text-destructive"/>
      404
    </h1>

    <p class="opacity-80 text-base">The page that you are looking for does not exist.</p>

    <div class="hover:scale-110 transition-all ease-in-out flex items-center gap-2 text-lg">
      <font-awesome-icon icon="fa-solid fa-chevron-left" class="text-2xl"/>
      <RouterLink
          to="/"
          class="underline">
        Go back to safety!
      </RouterLink>
    </div>
  </div>
</div>
</template>
