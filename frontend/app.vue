<script setup>
useHead({
  title: 'Climatlas',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
  charset: 'utf-8',
  meta: [
    { name: 'description', content: "Climatlas est un atlas de l'évolution du climat." }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    {
      rel: 'stylesheet',
      href: 'https://unpkg.com/maplibre-gl@1.15.2/dist/maplibre-gl.css'
    }
  ]
})
</script>

<template>
  <div>
    <NuxtPage />
  </div>
</template>
