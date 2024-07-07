import { createWebHashHistory, createRouter } from "vue-router";
import { isWeixin } from "./func";

const routes = [
    {
        path: "/",
        name: "index",
        component: () => import("./views/Index.vue"),
        children: [
            {
                path: "",
                name: "home",
                component: () => import("./views/Home.vue"),
                meta: {
                    title: "学生管理",
                    requiresAuth: true,
                    requireAdmin: false,
                },
            },
            {
                path: "admin",
                name: "admin",
                component: () => import("./views/Admin.vue"),
                redirect: { name: "userAdmin" },
                meta: {
                    title: "后台管理",
                    requiresAuth: true,
                    requireAdmin: true,
                },
                children: [
                    {
                        name: "userAdmin",
                        path: "user",
                        component: () => import("./components/UserMgmt.vue"),
                    },
                    {
                        name: "uploadExcel",
                        path: "upload",
                        component: () => import("./components/UploadExcel.vue"),
                    },
                    {
                        name: "uploadImage",
                        path: "image",
                        component: () => import("./components/UploadImage.vue"),
                    },
                    {
                        name: "delete",
                        path: "delete",
                        component: () => import("./components/Delete.vue"),
                    },
                ],
            },
        ],
    },
    {
        path: "/login",
        name: "login",
        component: () => import("./views/Login.vue"),
        meta: {
            title: "登录",
            requiresAuth: false,
            requireAdmin: false,
        },
    },
    {
        path: "/wx",
        name: "weixin",
        component: () => import("./views/Weixin.vue"),
        redirect: { name: "wx-welcome" },
        meta: {
            title: "学生管理",
            requiresAuth: false,
            requireAdmin: false,
            weixin: true,
        },
        children: [
            {
                name: "wx-welcome",
                path: "welcome",
                component: () => import("./components/WxWelcome.vue"),
            },
            {
                name: "wx-teacher",
                path: "teacher",
                component: () => import("./components/WxTeacher.vue"),
            },
            {
                name: "wx-student",
                path: "student",
                component: () => import("./components/WxStudent.vue"),
            },
        ],
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes,
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title;
    }
    if (!to.meta.weixin && isWeixin()) {
        return { path: "/wx/welcome" };
    }
    let token = sessionStorage.getItem("access_token_mystu");
    let admin = JSON.parse(sessionStorage.getItem("admin_mystu"));
    if ((!to.meta.requiresAuth && token) || (to.meta.requireAdmin && !admin)) {
        return {
            path: "/",
        };
    }
    if (to.meta.requiresAuth && !token) {
        return {
            path: "/login",
        };
    }
});

export default router;
