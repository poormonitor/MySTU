import { createWebHashHistory, createRouter } from "vue-router";
import { useUser } from "./store/user"
import pinia from "./store/store"

const routes = [
    {
        path: '/',
        name: "home",
        component: () => import("./views/Home.vue"),
        meta: {
            title: "学生管理",
            requiresAuth: true,
            requireAdmin: false
        }
    },
    {
        path: '/login',
        name: "login",
        component: () => import("./views/Login.vue"),
        meta: {
            title: "登录",
            requiresAuth: false,
            requireAdmin: false
        }
    },
    {
        path: '/admin',
        name: "admin",
        component: () => import("./views/Admin.vue"),
        meta: {
            title: "后台管理",
            requiresAuth: true,
            requireAdmin: true
        },
        children: [
            {
                name: "userAdmin",
                path: "user",
                component: () => import("./components/UserMgmt.vue")
            }
        ]
    }
]

const router = createRouter({ history: createWebHashHistory(), routes: routes })
const store = useUser(pinia)

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    let token = sessionStorage.getItem('access_token_mystu')
    if ((!to.meta.requiresAuth && token) || (to.meta.requireAdmin && !store.admin)) {
        return {
            path: "/"
        }
    }
    if (to.meta.requiresAuth && !token) {
        return {
            path: '/login',
        }
    }
})

export default router