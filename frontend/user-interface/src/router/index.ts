import { createRouter, createWebHistory } from 'vue-router'
import FileImporter from '../components/FileImporter.vue'
import HelloWorld from '../components/HelloWorld.vue'

const routes = [
  { path: '/', name: 'Hello', component: HelloWorld },
  { path: '/file_import', name: 'File Import', component: FileImporter },
]

const router = createRouter({
  history: createWebHistory(), // uses HTML5 history mode
  routes,
})

export default router
