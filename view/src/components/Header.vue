<script setup>
import { ref, h } from "vue"
import { IconFont } from 'tdesign-icons-vue-next';
import { useUser } from "../store/user"
import PasswordSetter from "./PasswordSetter.vue";
import Search from "./Search.vue"
import router from "../router"

const passwdChangerVisible = ref(false)
const SearchVisible = ref(false)
const emit = defineEmits(["updateStu"])
const store = useUser()

const logOut = () => {
    sessionStorage.removeItem("access_token_mystu")
    store.$reset()
    router.push({ name: "login" })
}

const changePassword = () => {
    passwdChangerVisible.value = true
}

const options = [
    { content: "后台管理", "prefix-icon": () => h(IconFont, { name: "control-platform" }), value: 3, click: () => { router.push({ name: "userAdmin" }) } },
    { content: "修改密码", "prefix-icon": () => h(IconFont, { name: "lock-on" }), value: 1, click: changePassword },
    { content: "退出登录", "prefix-icon": () => h(IconFont, { name: "logout" }), value: 2, click: logOut },
];

if (!store.admin) {
    options.shift()
}

const menuHandler = (data) => {
    options.find(item => item.value == data.value).click()
}

const updateInfo = (cls, id) => {
    emit("updateStu", cls, id)
    SearchVisible.value = false
}
</script>

<template>
    <PasswordSetter v-model:visible="passwdChangerVisible" />
    <Search v-model:visible="SearchVisible" @updateInfo="updateInfo" @confirm="SearchVisible = false" />
    <div class="bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 absolute h-14 w-full flex">
        <t-space>
            <router-link class="text-xl text-white font-semibold" :to="{ name: 'home' }">学生管理系统</router-link>
            <t-button variant="text" class="button-white ml-3 naviButton" @click="SearchVisible = true"
                v-if="this.$route.name == 'home'">搜索</t-button>
        </t-space>
        <div class="ml-auto justify-self-end">
            <t-dropdown :options="options" @click="menuHandler">
                <t-space>
                    <t-button variant="text" class="button-white">
                        {{ store.name }}
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