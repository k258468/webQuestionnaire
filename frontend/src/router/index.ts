import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CompletionView from '../views/CompletionView.vue';
import AdminView from '../views/AdminView.vue';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/complete', name: 'Complete', component: CompletionView },
  { path: '/admin', name: 'Admin', component: AdminView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});


