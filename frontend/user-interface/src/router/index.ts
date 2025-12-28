import { createRouter, createWebHistory } from 'vue-router'
import FileImporter from '../components/FileImporter.vue'
import Home from '../components/Home.vue'
import FaceRecognition from '../components/FaceRecognition.vue'
import AttendanceDashboard from '../components/AttendanceDashboard.vue'
import AttendanceReports from '../components/AttendanceReports.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/file_import', name: 'Register & Manage', component: FileImporter },
  { path: '/persons', redirect: '/file_import' }, // Redirect old route
  { path: '/recognize', name: 'Face Recognition', component: FaceRecognition },
  { path: '/attendance', name: 'Attendance', component: AttendanceDashboard },
  { path: '/reports', name: 'Reports', component: AttendanceReports },
]

const router = createRouter({
  history: createWebHistory(), // uses HTML5 history mode
  routes,
})

export default router
