import { createApp } from 'vue'
import App from './App.vue'
import PrimeVue from 'primevue/config';

const app = createApp(App);
app.use(PrimeVue);
// theme
import 'primevue/resources/themes/lara-light-indigo/theme.css';


app.mount('#app');