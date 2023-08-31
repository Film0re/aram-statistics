<template>
  <div class="centered">
    <Chart
      type="bar"
      :data="chartData"
    />
  </div>
</template>

<script setup>
import Chart from 'primevue/chart';
import { ref, computed, watch } from 'vue';
import { convertStatPropertyToLabel } from '../utils/utils.js';

const props = defineProps({
    data: {
        type: Array,
        required: true
    },
    stat : {
        type: Array,
        required: true
    }
});

const internalData = ref(props.data);
const stats = ref(props.stat);

// Better way to do this but this works for now

// Watch for changes in props data and sort internalData
watch(() => props.data, (newData) => {
    internalData.value = newData.slice().sort((a, b) => a[props.stat] - b[props.stat]);
});

// Watch for changes in props stat and sort internalData using the 
watch(() => props.stat, (newStat) => {
    stats.value = newStat;
    internalData.value = internalData.value.slice().sort((a, b) => a[newStat] - b[newStat]);
});

const chartData = computed(() => {
    const labels = internalData.value.map(champion => champion.champion_name);

    // Generate an array of pastel colors
    const pastelColors = [
            'rgb(75,193,181,0.2)',
            'rgb(207,65,71,0.2)',
            'rgb(74,189,85,0.2)',
            'rgb(153,89,203,0.2)',
            'rgb(129,177,77,0.2)',
            'rgb(208,86,184,0.2)',
            'rgb(186,177,58,0.2)',
            'rgb(97,109,205,0.2)',
            'rgb(218,147,52,0.2)',
            'rgb(94,147,205,0.2)',
            'rgb(212,89,45,0.2)',
            'rgb(70,147,94,0.2)',
            'rgb(214,69,129,0.2)',
            'rgb(118,121,50,0.2)',
            'rgb(204,144,209,0.2)',
            'rgb(158,95,47,0.2)',
            'rgb(148,81,140,0.2)',
            'rgb(215,161,109,0.2)',
            'rgb(160,70,86,0.2)',
            'rgb(226,127,135,0.2)'
        ];

    if(stats.value.length == 0 ){
        return;
    }

    const datasets = stats.value.map((stat, index) => {
        const data = internalData.value.map(champion => champion[stat]);
        const backgroundColor = pastelColors[index % pastelColors.length];

        return {
            label: convertStatPropertyToLabel(stat), // Use the label conversion function
            data: data,
            backgroundColor: backgroundColor,
            borderColor: backgroundColor.replace('0.2', '1'),
            borderWidth: 1
        };
    });

    return {
        labels: labels,
        datasets: datasets
    };
});

</script>

<style scoped>
/* Your styles here */
</style>
