<script setup lang="ts">
import { Toaster } from 'vue-sonner'
import Navigation from '@/components/Navigation.vue'
import 'vue-sonner/style.css'
</script>

<template>
  <Navigation />
  <router-view />
  <Toaster />
</template>
