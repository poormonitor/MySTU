<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { DesktopIcon, LockOnIcon } from "tdesign-icons-vue-next";
import { MessagePlugin } from "tdesign-vue-next";
import axios from "../axios";
import sha256 from "crypto-js/sha256";

const router = useRouter();
const account = ref();
const password = ref();
const loading = ref(false);

const loginRequest = () => {
    loading.value = true;
    axios
        .post("/login", {
            user: account.value,
            passwd: sha256(password.value).toString(),
        })
        .catch(() => {
            loading.value = false;
        })
        .then((response) => {
            if (response.data.status == "ok") {
                let data = response.data.data;
                sessionStorage.setItem("access_token_mystu", data.access_token);
                sessionStorage.setItem("user_mystu", account.value);
                sessionStorage.setItem("name_mystu", data.name);
                sessionStorage.setItem("admin_mystu", data.admin);
                loading.value = false;
                router.push({ name: "home" });
            } else {
                MessagePlugin.error(response.data.data.msg);
                loading.value = false;
            }
        });
};
</script>
<template>
    <div
        class="py-12 lg:py-16 bg-gradient-to-br from-cyan-50 to-blue-200 min-h-full"
    >
        <div
            class="text-center text-4xl lg:text-5xl mb-3 px-6 font-bold tracking-widest"
        >
            学生管理系统
        </div>
        <div
            class="bg-white flex flex-col lg:flex-row rounded-2xl shadow-xl mx-10 lg:mx-24 mt-8 lg:mt-16 divide-y lg:divide-x lg:divide-y-0"
        >
            <div class="mb-8 mx-4 flex justify-center items-center lg:w-2/5">
                <div class="p-8 lg:p-12 mx-auto">
                    <div class="text-center text-2xl font-semibold mt-3 mb-6">
                        登录
                    </div>
                    <t-form>
                        <t-input
                            size="large"
                            label="账号"
                            placeholder="账号"
                            v-model="account"
                            class="mt-12"
                            autocomplete="username"
                        >
                            <template #prefix-icon>
                                <desktop-icon />
                            </template>
                        </t-input>
                        <t-input
                            size="large"
                            label="密码"
                            placeholder="密码"
                            v-model="password"
                            type="password"
                            class="my-6"
                            @enter="loginRequest"
                            autocomplete="current-password"
                        >
                            <template #prefix-icon>
                                <lock-on-icon />
                            </template>
                        </t-input>
                    </t-form>
                    <div class="flex justify-center">
                        <t-button
                            @click="loginRequest"
                            class="mt-4"
                            :loading="loading"
                            size="large"
                        >
                            登录
                        </t-button>
                    </div>
                </div>
            </div>
            <div class="lg:py-20 py-10 px-12 flex-wrap lg:w-3/5">
                <p
                    class="lg:leading-relaxed font-semibold text-2xl lg:text-4xl text-transparent bg-clip-text bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500"
                >
                    世界上没有才能的人是没有的。问题在于教育者要去发现每一位学生的禀赋、兴趣、爱好和特长，为他们的表现和发展提供充分的条件和正确引导。
                </p>
                <p
                    class="pt-4 lg:pt-8 text-xl lg:text-3xl font-bold text-right text-stone-600"
                >
                    苏霍姆林斯基
                </p>
            </div>
        </div>
    </div>
</template>
