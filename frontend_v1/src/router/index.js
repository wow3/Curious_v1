import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'
import axios from 'axios'

import Login from "../components/Login.vue";
import Register from "../components/Register";

import Answer from "../components/Answer";
import Notification from "../components/Notification";
import Space from "../components/Space";
import Home from "../components/Home";
import Profile from "../components/Profile";
import Admin from "../components/Admin";

Vue.use(VueRouter)

  const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home
  // },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // },
      // 重定向
    {
      path: '/',
      redirect: '/login'
    },
      // 登录
    {
      path: '/login',
      component: Login
    },
      // 注册
    {
      path: '/register',
      component: Register
    },
      // 管理员页面
    {
      path: '/admin',
      component: Admin
    },
      // root
    {
      path: '/index',
      component: Index,
      children: [
          // 主页
        {
          path: '/home',
          component: Home
        },
        // 回答
        {
          path: '/answer',
          component: Answer
        },
        // 空间
        {
          path: '/space',
          component: Space
        },
        // 信息
        {
          path: '/notification',
          component: Notification
        },
        // 个人
        {
          path: '/profile',
          component: Profile
        }
      ]
    }
]

const router = new VueRouter({
  routes
})

// 挂载路由导航守卫
// router.beforeEach((to, from, next) => {
//   if(to.path === '/login') return next()
//   // 获取token
//   const tokenStr = sessionStorage.getItem('token')
//   if(!tokenStr) return next('/login')
//   next()
// })

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}


export default router
