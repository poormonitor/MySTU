<script setup>
import { reactive } from "vue";
import axios from "../axios";

const studentInfo = reactive({
    sid: "",
    phone: "",
});

const bind = () => {
    let state = encodeURIComponent(btoa(JSON.stringify(studentInfo)));
    let current_url = location.origin + "/api/wx/add";
    current_url = encodeURIComponent(current_url);
    axios.get("/wx/appid").then((response) => {
        if (response.data.status != "ok") return;
        let appid = response.data.data.appid;
        window.location.href =
            "https://open.weixin.qq.com/connect/oauth2/authorize?" +
            `appid=${appid}` +
            `&redirect_uri=${current_url}` +
            "&response_type=code" +
            "&scope=snsapi_userinfo" +
            `&state=${state}` +
            "#wechat_redirect";
    });
};
</script>

<template>
    <div class="my-6 mx-4">
        <t-card>
            <template #title>
                <div class="text-lg">绑定微信</div>
            </template>
            <template #content>
                <div class="mb-6">
                    <t-form>
                        <t-form-item label="学号">
                            <t-input v-model="studentInfo.sid" />
                        </t-form-item>
                        <t-form-item label="家长手机号">
                            <t-input v-model="studentInfo.phone" />
                        </t-form-item>
                    </t-form>
                </div>

                <div class="text-center">
                    <t-button @click="bind">绑定微信</t-button>
                </div>
            </template>
        </t-card>
    </div>
    <div class="text-center text-xs text-neutral-600">
        教师/辅导员，请使用管理系统菜单中的二维码绑定。
    </div>
</template>
