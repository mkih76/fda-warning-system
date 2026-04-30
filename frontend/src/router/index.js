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

    // ═══ 制药板块 ═══
    {
      path: '/pharma',
      name: 'pharma-home',
      component: () => import('../views/pharma/PharmaHome.vue'),
    },
    {
      path: '/pharma/:category',
      name: 'pharma-list',
      component: () => import('../views/pharma/PharmaArticleList.vue'),
    },
    {
      path: '/pharma/article/:slug',
      name: 'pharma-article',
      component: () => import('../views/pharma/PharmaArticleDetail.vue'),
    },

    // ═══ 化妆品板块 ═══
    {
      path: '/cosmetics',
      name: 'cosmetics-home',
      component: () => import('../views/cosmetics/CosmeticsHome.vue'),
    },
    {
      path: '/cosmetics/:category',
      name: 'cosmetics-list',
      component: () => import('../views/cosmetics/CosmeticsArticleList.vue'),
    },
    {
      path: '/cosmetics/article/:slug',
      name: 'cosmetics-article',
      component: () => import('../views/cosmetics/CosmeticsArticleDetail.vue'),
    },

    // ═══ 食品板块 ═══
    {
      path: '/food',
      name: 'food-home',
      component: () => import('../views/food/FoodHome.vue'),
    },
    {
      path: '/food/:category',
      name: 'food-list',
      component: () => import('../views/food/FoodArticleList.vue'),
    },
    {
      path: '/food/article/:slug',
      name: 'food-article',
      component: () => import('../views/food/FoodArticleDetail.vue'),
    },

    // ═══ 综合板块 ═══
    {
      path: '/general',
      name: 'general-home',
      component: () => import('../views/general/GeneralHome.vue'),
    },

    // ═══ 工具 ═══
    {
      path: '/tools',
      name: 'tools-home',
      component: () => import('../views/tools/ToolsHome.vue'),
    },

    // ═══ 关于 ═══
    {
      path: '/about',
      name: 'about-home',
      component: () => import('../views/about/AboutHome.vue'),
    },

    // ═══ 认证 ═══
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginPage.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterPage.vue'),
    },
  ],
})

export default router
