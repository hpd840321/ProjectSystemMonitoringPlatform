import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/projects',
      name: 'projects',
      component: () => import('@/views/project/ProjectList.vue')
    },
    {
      path: '/projects/:id',
      name: 'project-detail',
      component: () => import('@/views/project/ProjectDetail.vue')
    },
    {
      path: '/projects/:projectId/servers/:serverId',
      name: 'server-detail',
      component: () => import('@/views/project/server/ServerDetail.vue')
    },
    {
      path: '/backup',
      name: 'backup',
      component: () => import('@/views/backup/BackupList.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: '系统备份'
      }
    },
    {
      path: '/logs',
      name: 'logs',
      component: () => import('@/views/log/LogList.vue'),
      meta: {
        requiresAuth: true,
        title: '日志查看'
      }
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/settings/SystemSettings.vue'),
      meta: {
        requiresAuth: true,
        requiresAdmin: true,
        title: '系统设置'
      }
    }
  ]
})

export default router 