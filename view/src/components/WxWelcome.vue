<script setup>
import { useRouter, useRoute } from "vue-router";
import axios from "../axios";

const router = useRouter();
const route = useRoute();
const token = sessionStorage.getItem("access_token_mystu");

if (token) {
    let role = sessionStorage.getItem("role_mystu");
    if (role == "0") router.push({ name: "wx-teacher" });
    else router.push({ name: "wx-student" });
}

if (route.query.token) {
    let token = route.query.token;
    let role = route.query.role;
    sessionStorage.setItem("access_token_mystu", token);
    sessionStorage.setItem("role_mystu", role);
    if (role == 0) router.push({ name: "wx-teacher" });
    else router.push({ name: "wx-student" });
} else {
    let current_url = location.origin + "/api/wx/login";
    current_url = encodeURIComponent(current_url);
    axios.get("/wx/appid").then((response) => {
        if (response.data.status != "ok") return;
        let appid = response.data.data.appid;
        window.location.href =
            "https://open.weixin.qq.com/connect/oauth2/authorize?" +
            `appid=${appid}` +
            `&redirect_uri=${current_url}` +
            "&response_type=code" +
            "&scope=snsapi_base" +
            "#wechat_redirect";
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
            ></t-loading>
        </div>
    </div>
</template>
