import { createWebHashHistory, createRouter } from "vue-router";

const routes = [
    {
        path: '/',
        name: "home",
        component: () => import("./views/Home.vue"),
        meta: {
            title: "谈话管理",
            requiresAuth: true
        }
    },
    {
        path: '/login',
        name: "login",
        component: () => import("./views/Login.vue"),
        meta: {
            title: "登录",
            requiresAuth: false
        }
    }
]

const router = createRouter({ history: createWebHashHistory(), routes: routes })

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    let token = sessionStorage.getItem('access_token_mystu')
    if (!to.meta.requiresAuth && token) {
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