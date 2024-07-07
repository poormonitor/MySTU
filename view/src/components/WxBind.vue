<script setup>
import { useRoute } from "vue-router";

const route = useRoute();

const appid = import.meta.env.VITE_APPID;
const appsecret = import.meta.env.VITE_APPSECRET;

const failed = ref(false);

if (!route.params.code) {
    let current_url = "https://stu.techo.cool/#/m";
    current_url = encodeURIComponent(current_url);
    let token = route.params.token;
    window.location.href =
        "https://open.weixin.qq.com/connect/oauth2/authorize?" +
        `appid=${appid}` +
        `&redirect_uri=${current_url}` +
        "&response_type=code" +
        "&scope=snsapi_base" +
        `&state=${token}` +
        "#wechat_redirect";
} else {
    axios({
        method: "get",
        url: "https://api.weixin.qq.com/sns/oauth2/access_token",
        params: {
            code: route.params.code,
            appid: appid,
            secret: appsecret,
            grant_type: "authorization_code",
        },
    }).then((response) => {
        let open_id = response.data.open_id;
        let token = route.params.state;

        axios({
            method: "post",
            url: "/wx/bind",
            data: {
                openid: open_id,
                access_token: token,
            },
        }).then((response) => {
            if (response.data.status == "ok") {
                router.push({ name: "wx-welcome" });
            } else {
                failed.value = true;
            }
        });
    });
}
</script>

<template>
    <div class="flex justify-center items-center h-screen">
        <div class="text-center">
            <t-loading
                class="mt-6 flex justify-center"
                text="绑定中..."
                size="small"
                v-if="!failed"
            ></t-loading>
            <div class="mt-6 text-xl font-semibold text-center" v-else>
                绑定失败，请联系管理员
            </div>
        </div>
    </div>
</template>
