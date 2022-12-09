import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PageNotFound from '../views/PageNotFound.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/stories/:storyType?',
        name: 'stories',
        component: () => import('@/views/StoriesView.vue')
    },
    {
        path: '/story',
        name: 'story',
        component: () => import('@/views/StoryView.vue')
    },
    {
        path: '/courses',
        name: 'courses',
        component: () => import('@/views/CoursesView.vue')
    },
    {
        path: '/course',
        name: 'course',
        component: () => import('@/views/CourseView.vue')
    },
    {
        path: '/lecture',
        name: 'lecture',
        component: () => import('@/views/LectureView.vue')
    },
    {
        path: '/contacts',
        name: 'contacts',
        component: () => import('@/views/ContactsView.vue')
    },
    {
        path: '/forms',
        name: 'forms',
        component: () => import('@/views/FormsView.vue')
    },
    {
        path: "/:catchAll(.*)",
        component: PageNotFound
    },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
