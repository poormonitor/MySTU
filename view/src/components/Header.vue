<script setup>
import { ref, h } from "vue";
import {
    ControlPlatformIcon,
    LockOnIcon,
    LogoutIcon,
    ChevronDownIcon,
} from "tdesign-icons-vue-next";
import { useRouter } from "vue-router";
import { logOut } from "../func";
import PasswordSetter from "./PasswordSetter.vue";

const router = useRouter();

const passwdChangerVisible = ref(false);

const logOutFunc = () => {
    logOut();
    router.push({ name: "login" });
};

const changePassword = () => {
    passwdChangerVisible.value = true;
};

let options = [
    {
        content: "后台管理",
        "prefix-icon": () => h(ControlPlatformIcon, { class: "w-1.5 h-1.5" }),
        value: 3,
        click: () => {
            router.push({ name: "userAdmin" });
        },
    },
    {
        content: "修改密码",
        "prefix-icon": () => h(LockOnIcon, { class: "w-1.5 h-1.5" }),
        value: 1,
        click: changePassword,
    },
    {
        content: "退出登录",
        "prefix-icon": () => h(LogoutIcon, { class: "w-1.5 h-1.5" }),
        value: 2,
        click: logOutFunc,
    },
];

if (!JSON.parse(sessionStorage.getItem("admin_mystu"))) {
    options.shift();
}

const menuHandler = (data) => {
    options.find((item) => item.value == data.value).click();
};

const currentUser = sessionStorage.getItem("name_mystu");
</script>

<template>
    <PasswordSetter v-model:visible="passwdChangerVisible" />
    <div
        class="bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 absolute h-14 w-full flex"
    >
        <t-space>
            <router-link
                class="text-xl text-white font-semibold"
                :to="{ name: 'home' }"
                >学生管理系统</router-link
            >
        </t-space>
        <div class="ml-auto justify-self-end">
            <t-dropdown :options="options" @click="menuHandler">
                <t-space>
                    <t-button variant="text" class="button-white">
                        {{ currentUser }}
                        <template #suffix>
                            <ChevronDownIcon class="w-1.5 h-1.5" />
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
    background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>
