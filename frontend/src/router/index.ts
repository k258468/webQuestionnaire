import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CompletionView from '../views/CompletionView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/complete', component: CompletionView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});


