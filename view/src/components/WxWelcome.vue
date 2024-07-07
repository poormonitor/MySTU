<script setup>
import { useRouter, useRoute } from "vue-router";

const appid = import.meta.env.VITE_APPID;

const router = useRouter();
const route = useRoute();
const token = sessionStorage.getItem("token_mystu");

if (token) {
    let role = sessionStorage.getItem("role_mystu");
    if (role == "0") router.push({ name: "wx-teacher" });
    else router.push({ name: "wx-student" });
}

if (route.params.token) {
    let token = route.params.token;
    let role = route.params.role;
    sessionStorage.setItem("token_mystu", token);
    sessionStorage.setItem("role_mystu", role);
    if (role == 0) router.push({ name: "wx-teacher" });
    else router.push({ name: "wx-student" });
} else {
    let current_url = location.origin + "/api/wx/login";
    current_url = encodeURIComponent(current_url);
    window.location.href =
        "https://open.weixin.qq.com/connect/oauth2/authorize?" +
        `appid=${appid}` +
        `&redirect_uri=${current_url}` +
        "&response_type=code" +
        "&scope=snsapi_base" +
        "#wechat_redirect";
}
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        <div class="text-center">
            <t-loading
                class="mt-6 flex justify-center"
                text="正在登录..."
                size="small"
            ></t-loading>
        </div>
    </div>
</template>
