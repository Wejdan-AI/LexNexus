<template>
  <main
    class="relative flex flex-col items-center justify-center min-h-screen py-10"
  >
    <a
      href="/"
      class="px-6 py-2 text-sm font-medium text-gray-600 transition-all rounded-full shadow-sm bg-white/30 dark:bg-white/80 ring-1 ring-gray-900/5 dark:text-black hover:shadow-lg active:shadow-sm mb-4"
    >
      ← Back to Home
    </a>
    <h1
      class="pt-4 pb-8 bg-gradient-to-br dark:from-white from-black via-[#707070] to-[#ffffff] bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl"
    >
      LexNexus Clauses
    </h1>
    <ClauseTable :clauses="data?.clauses" :duration="data?.duration" />
    <div
      class="w-full max-w-lg mt-6 font-light text-center text-gray-600 dark:text-gray-300"
    >
      Browse and manage legal clauses
      <div class="flex items-center justify-center my-2">
        <span>Powered by</span>
        <a
          href="https://nuxt.com/docs"
          class="flex items-center font-medium underline transition-colors underline-offset-4 dark:hover:text-white hover:text-black"
        >
          <img src="/nuxt.svg" class="h-6 mx-2" />
          <p>Nuxt</p>
        </a>
      </div>
    </div>
  </main>
</template>

<script setup>
const { data } = useFetch('/api/get-clauses')
</script>
