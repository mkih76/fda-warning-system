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
      component: () => import('../views/Letters.vue'),
    },
    {
      path: '/letters/:id',
      name: 'letter-detail',
      component: () => import('../views/LetterDetail.vue'),
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboard.vue'),
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
