<template>
  <Card class="champion-card">
    <template #title>
      #{{ index }}  {{ props.champion.champion_name }} - {{ props.champion.games_played }} Games 
    </template>
    <template #content>
      <div
        v-for="(value, key) in props.champion"
        :key="key"
      >
        <template v-if="stats.includes(key) && (key != 'games_played')">
          {{ convertStatPropertyToLabel(key) }}: {{ value.toFixed(2) }}
        </template>
      </div>
    </template>
  </Card>
</template>

<script setup>
import Card from 'primevue/card';
import { convertStatPropertyToLabel } from '../utils/utils.js';

const props = defineProps({
  champion: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  stats: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.champion-card {
    width: 20em;
    margin: 1em;
}
</style>
