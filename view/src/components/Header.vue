<script setup>
import { ref, h } from "vue"
import { IconFont } from 'tdesign-icons-vue-next';
import { useRouter } from "vue-router"
import { logOut } from "../func"
import PasswordSetter from "./PasswordSetter.vue";

const router = useRouter()

const passwdChangerVisible = ref(false)

const logOutFunc = () => {
    logOut()
    router.push({ name: "login" })
}

const changePassword = () => {
    passwdChangerVisible.value = true
}

const options = [
    { content: "后台管理", "prefix-icon": () => h(IconFont, { name: "control-platform" }), value: 3, click: () => { router.push({ name: "userAdmin" }) } },
    { content: "修改密码", "prefix-icon": () => h(IconFont, { name: "lock-on" }), value: 1, click: changePassword },
    { content: "退出登录", "prefix-icon": () => h(IconFont, { name: "logout" }), value: 2, click: logOutFunc },
];

if (!sessionStorage.getItem("admin_mystu")) {
    options.shift()
}

const menuHandler = (data) => {
    options.find(item => item.value == data.value).click()
}

const currentUser = sessionStorage.getItem("name_mystu")
</script>

<template>
    <PasswordSetter v-model:visible="passwdChangerVisible" />
    <div class="bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 absolute h-14 w-full flex">
        <t-space>
            <router-link class="text-xl text-white font-semibold" :to="{ name: 'home' }">学生管理系统</router-link>
        </t-space>
        <div class="ml-auto justify-self-end">
            <t-dropdown :options="options" @click="menuHandler">
                <t-space>
                    <t-button variant="text" class="button-white">
                        {{ currentUser }}
                        <template #suffix>
                            <icon-font name="chevron-down" class="text-white" size="16" />
                        </template>
                    </t-button>
                </t-space>
            </t-dropdown>
        </div>
    </div>
</template>
<style>
.button-white {
    color: white !important;
    background: transparent !important;
    border: 0 !important;
}

.naviButton:hover {
    background-color: rgba(255, 255, 255, 0.1) !important
}
</style>