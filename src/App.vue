<template>
  <MainView />
  <Footer />
</template>

<script setup>
import MainView from './views/MainView.vue';
import Footer from './components/Footer.vue';

</script>

<style>
#champion-cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

#app{
  width: 90%;
  margin: 0 auto;
}

body {
    font-family: var(--font-family);
} 
</style>
