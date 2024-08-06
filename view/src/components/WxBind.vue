<script setup>
import { useRoute } from "vue-router";
import axios from "../axios";

const route = useRoute();

let current_url = location.origin + "/api/wx/bind";
current_url = encodeURIComponent(current_url);
let token = encodeURIComponent(route.query.token);

axios.get("/wx/appid").then((response) => {
    if (response.data.status != "ok") return;
    let appid = response.data.data.appid;
    window.location.href =
        "https://open.weixin.qq.com/connect/oauth2/authorize?" +
        `appid=${appid}` +
        `&redirect_uri=${current_url}` +
        "&response_type=code" +
        "&scope=snsapi_userinfo" +
        `&state=${token}` +
        "#wechat_redirect";
});
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        <div class="text-center">
            <t-loading
                class="mt-6 flex justify-center"
                text="绑定中..."
                size="small"
            ></t-loading>
        </div>
    </div>
</template>
