import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeNew.vue'),
    },
    {
      path: '/letters',
      name: 'letters',
      component: () => import('../views/LettersNew.vue'),
    },
    {
      path: '/letters/:id',
      name: 'letter-detail',
      component: () => import('../views/LetterDetailNew.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardNew.vue'),
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('../views/Favorites.vue'),
    },
    {
      path: '/regulations',
      name: 'regulations',
      component: () => import('../views/Regulations.vue'),
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('../views/News.vue'),
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('../views/Articles.vue'),
    },
  ],
})

export default router
