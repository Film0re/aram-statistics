<template>
  <div class="center-text">
    {{ summoner.name }}'s Best Aram Champions {{ summoner.region }} - {{ totalGames }} Games ({{ winRate.toFixed(2) }}%)
  </div>
  <Toolbar>
    <template #center>
      <div id="toolbar-center">
        <div class="toolbar-item">
          <label for="summoner-name-dropdown">Summoner Name:</label>
          <Dropdown
            id="summoner-name-dropdown"
            v-model="summonerName"
            :options="summonerNameOptions"
          />
        </div>

        <div class="toolbar-item">
          <OverlayPanel ref="statOverlayPanel">
            <div class="center-text">
              Toggle Stats to be Displayed
            </div>

            <div class="overlay-panel-content">
              <div class="overlay-panel-column">
                <Listbox
                  v-model="statsColumn1"
                  :options="statOptionsColumn1"
                  multiple="multiple"
                  :option-label="convertStatPropertyToLabel"
                />
              </div>

              <div class="overlay-panel-column">
                <Listbox
                  v-model="statsColumn2"
                  :options="statOptionsColumn2"
                  multiple="multiple"
                  :option-label="convertStatPropertyToLabel"
                />
              </div>
            </div>
          </OverlayPanel>
        </div>

        <div class="toolbar-item">
          <label for="stat-dropdown"> Sort By:</label>
          <Dropdown
            id="stat-dropdown"
            v-model="statToSortBy"
            :options="stats"
            :option-label="convertStatPropertyToLabel"
          />
        </div>

        <Button
          label="Pick Stats"
          @click="toggleOverlayPanel"
        />

        <div class="toolbar-item">
          <label for="number-of-champions">Number of Champions:</label>
          <InputNumber
            id="number-of-champions"
            v-model="numberOfChampions"
            input-id="stacked-buttons"
            show-buttons
            :min="1"
            :max="167"
          />
        </div>
      </div>
    </template>
  </Toolbar>

  <TabView>
    <TabPanel header="Champion Statistic Cards">
      <div id="champion-cards-container">
        <ChampionCard
          v-for="champion in champions"
          :key="champion.champion_id"
          :stats="stats"
          :champion="champion"
          :index="champions.indexOf(champion) + 1"
        />
      </div>
    </TabPanel>

    <TabPanel header="Champion Statistics Chart">
      <div class="center">
        <ChampionsChart
          :data="champions"
          :stat="stats"
          class="champion-chart"
        />
      </div>
    </TabPanel>
  </TabView>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { supabase } from '../lib/supabaseClient';
import { watch } from 'vue';
import { convertStatPropertyToLabel } from '../utils/utils.js';
import ChampionCard from '../components/ChampionCard.vue';
import ChampionsChart from '../components/ChampionsChart.vue';
import Toolbar from 'primevue/toolbar';
import Dropdown from 'primevue/dropdown';
import InputNumber from 'primevue/inputnumber';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Button from 'primevue/button';
import Listbox from 'primevue/listbox';
import OverlayPanel from 'primevue/overlaypanel';

// Overlays 
const statOverlayPanel = ref(null);

const toggleOverlayPanel = (event) => {
  statOverlayPanel.value.toggle(event);
}

const statsColumn1 = ref(['wins', 'games_played', 'win_percent', 'avg_kda', 'avg_kills', 'avg_assists', 'avg_deaths']); // Initialize the first column with a default stat
const statsColumn2 = ref([]); // Initialize the second column with no default stats
const stats = ref(['games_played', 'wins', 'win_percent', 'avg_kda', 'avg_kills', 'avg_assists', 'avg_deaths', ]);

// Split stat options into two columns
const splitStatOptions = () => {
  const middleIndex = Math.ceil(statOptions.value.length / 2);
  statOptionsColumn1.value = statOptions.value.slice(0, middleIndex);
  statOptionsColumn2.value = statOptions.value.slice(middleIndex);
};

const summoner = ref({});
const summonerName = ref('Film0re'); 
const summonerNameOptions = ref([]);

const champions = ref([]); // Array of champions to show
const championBuffer = ref([]); // Array of champions to hold all champions
const totalGames = ref(0);
const numberOfChampions = ref(12); // Number of champions to show
const numberOfChampionsToFetch = ref(12); // Number of champions to fetch
const statOptions = ref([])
const winRate = ref(0);

const statOptionsColumn1 = ref([]);
const statOptionsColumn2 = ref([]);


// watch stats and split into two columns
watch([statsColumn1, statsColumn2], ([newStatsColumn1, newStatsColumn2]) => {
  stats.value = [...newStatsColumn1, ...newStatsColumn2];
});

// watch summoner region and fetch new data
const fetchSummoner = async () => {
  const { data, error } = await supabase
    .from('summoners')
    .select('*')
    .eq('name', summoner.value.name)
    .eq('region', summoner.value.region)
    .limit(1)
    .single();
  if (error) {
    console.log(error);
  } else {
    summoner.value = data;
  }
};

// watch summoner name and fetch new data
watch(summonerName, async (newSummonerName) => {
  summoner.value.name = newSummonerName;
  await fetchSummoner();
  const summoner_id = summoner.value.summoner_id;
  await fetchNumberOfGamesPlayed();
  await fetchChampionData(summoner_id);
});

// watch number of champions and fetch new data
watch(numberOfChampions, async (newNumberOfChampions) => {
  const summoner_id = summoner.value.summoner_id;

  if (newNumberOfChampions > championBuffer.value.length) {
    numberOfChampionsToFetch.value = newNumberOfChampions * 2; // Fetch double the number of champions
    await fetchChampionData(summoner_id);
    return;
  }

  if (newNumberOfChampions > championBuffer.value.length) {
    await fetchChampionData(summoner_id);
    return;
  }

  champions.value = championBuffer.value.slice(0, newNumberOfChampions);
});

const statToSortBy = ref('games_played');

// watch stat and sort champions
watch(statToSortBy, (newStat) => {
  // championBuffer.value.sort((a, b) => b[newStat] - a[newStat]);
  // The reason it is not done as above is beause I want to make sure the champions have a decent number of games played
  // The less games are played the more useless the stat is
  champions.value = championBuffer.value.slice(0, numberOfChampions.value);
  champions.value.sort((a, b) => b[newStat] - a[newStat]);
});




// Grabs Champion 
const fetchChampionData = async (summoner_id) => {
  const { data, error } = await supabase.rpc('get_top_champions_stats_test', {
    summoner_id_param : summoner_id,
    top_count_param : numberOfChampionsToFetch.value || 1000
  });

  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }

  championBuffer.value = data;
  
  champions.value = championBuffer.value.slice(0, numberOfChampions.value);
  // Create stat options dynamically
  statOptions.value = Object.keys(data[0]).filter(key => key !== 'champion_name' && key !== 'champion_id');
  return data;
}

const fetchNumberOfGamesPlayed = async () => {
  const { data, error } = await supabase.rpc('calculate_win_percent_and_games', {
    summoner_id_param : summoner.value.summoner_id
  });

  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }

  totalGames.value = data[0].games_played_count;
  winRate.value = data[0].win_percent;
}

const fetchSummoners = async () => {
  const { data, error } = await supabase.rpc('get_summoners');

  if (error) {
    console.error('Error fetching data:', error);
    return null;
  }

  summonerNameOptions.value = data.map(summoner => summoner.name);
}
onMounted(async () => {
  summoner.value.region = 'NA';
  summoner.value.name = 'Film0re';
  await fetchSummoner();
  const summoner_id = summoner.value.summoner_id;

  await fetchNumberOfGamesPlayed();
  await fetchChampionData(summoner_id);
  await fetchSummoners();
  splitStatOptions();
});
</script>

<style scoped>
label{
  font-size: 1.5rem;
  margin-right: 1rem;
}

#toolbar-center {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

.toolbar-item {
  margin: .5rem;
}

.overlay-panel-content {
  display: flex;
}

.overlay-panel-column {
  flex: 1;
  padding: 0 1rem;
}

.center-text {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem;
}

.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.champion-chart {
  width: 75%;
  height: 70%;
}

.center-screen {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
