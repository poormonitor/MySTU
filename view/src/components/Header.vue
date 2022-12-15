<script setup>
import { ref, computed, h } from "vue"
import { IconFont } from 'tdesign-icons-vue-next';
import PasswordSetter from "./PasswordSetter.vue";
import { useRouter } from "vue-router"

const router = useRouter()
const passwdChangerVisible = ref(false)

const logOut = () => {
    sessionStorage.removeItem("access_token_mystu")
    sessionStorage.removeItem("user_mystu")
    router.push({ name: "login" })
}

const changePassword = () => {
    passwdChangerVisible.value = true
}

const options = [
    { content: "修改密码", "prefix-icon": () => h(IconFont, { name: "lock-on" }), value: 1, click: changePassword },
    { content: "退出登录", "prefix-icon": () => h(IconFont, { name: "logout" }), value: 2, click: logOut },
];

const menuHandler = (data) => {
    options.find(item => item.value == data.value).click()
}

const currentUser = computed(() => sessionStorage.getItem("user_mystu"))
</script>

<template>
    <PasswordSetter v-model:visible="passwdChangerVisible" />
    <div class="bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 absolute h-14 w-full flex">
        <span class="text-xl text-white font-semibold">学生管理系统</span>
        <div class="ml-auto justify-self-end">
            <t-dropdown :options="options" @click="menuHandler">
                <t-space>
                    <t-button variant="text" class="button-dropdown">
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
.button-dropdown {
    color: white !important;
    background: transparent !important;
    border: 0 !important;
}
</style>