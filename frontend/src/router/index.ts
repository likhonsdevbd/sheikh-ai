import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/App.vue'),
    meta: {
      title: 'Sheikh AI Assistant'
    }
  },
  {
    path: '/chat/:sessionId?',
    name: 'Chat',
    component: () => import('@/App.vue'),
    meta: {
      title: 'Chat - Sheikh AI'
    }
  },
  {
    path: '/sessions',
    name: 'Sessions',
    component: () => import('@/App.vue'),
    meta: {
      title: 'Sessions - Sheikh AI'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/App.vue'),
    meta: {
      title: 'Settings - Sheikh AI'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title as string
  }
  
  next()
})

export default router