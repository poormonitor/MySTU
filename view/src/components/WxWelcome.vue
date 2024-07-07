<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref } from "vue";
import axios from "../axios";

const appid = import.meta.env.VITE_APPID;

const router = useRouter();
const route = useRoute();
const token = sessionStorage.getItem("token_mystu");
const failed = ref(false);

if (token) {
    let role = sessionStorage.getItem("role_mystu");
    if (role == "0") router.push({ name: "wx-teacher" });
    else router.push({ name: "wx-student" });
}

if (!token || route.params.code) {
    let current_url = "https://stu.techo.cool/#/m";
    current_url = encodeURIComponent(current_url);
    window.location.href =
        "https://open.weixin.qq.com/connect/oauth2/authorize?" +
        `appid=${appid}` +
        `&redirect_uri=${current_url}` +
        "&response_type=code" +
        "&scope=snsapi_base" +
        "#wechat_redirect";
}

if (route.params.code) {
    axios.post("/wx/login", { code: route.params.route }).then((response) => {
        if (response.data.status == "ok") {
            let token = response.data.data.access_token;
            let role = response.data.data.role;
            sessionStorage.setItem("token_mystu", token);
            sessionStorage.setItem("role_mystu", role);
            if (role == 0) router.push({ name: "wx-teacher" });
            else router.push({ name: "wx-student" });
        } else {
            failed.value = true;
        }
    });
}
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        <div class="text-center">
            <t-loading
                class="mt-6 flex justify-center"
                text="正在登录..."
                size="small"
                v-if="!failed"
            ></t-loading>
            <div class="mt-6 text-xl font-semibold text-center" v-else>
                登录失败，请联系管理员
            </div>
        </div>
    </div>
</template>
