<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import axios from "../axios"
import swal from "sweetalert"
import sha256 from 'crypto-js/sha256'

const account = ref()
const password = ref()
const router = useRouter()
const loading = ref(false)

const loginRequest = () => {
    loading.value = true
    axios.post("/login", {
        user: account.value,
        passwd: sha256(password.value).toString()
    }).catch(() => {
        swal({
            title: "请求失败",
            text: "您的请求失败，请检查网络",
            icon: "error"
        }).then(() => {
            loading.value = false
        })
    }).then((response) => {
        if (response.data.status == "ok") {
            let access_token = response.data.data.access_token
            sessionStorage.setItem("access_token_mystu", access_token)
            sessionStorage.setItem("user_mystu", account.value)
            loading.value = false
            router.push({ name: "home" })
        } else {
            swal({
                title: response.data.error.title,
                text: response.data.error.text,
                icon: response.data.error.icon
            }).then(() => {
                loading.value = false
            })
        }
    })
}
</script>
<template>
    <div class="py-16">
        <div class="text-center text-4xl md:text-5xl mb-3 px-6 font-bold tracking-widest">浙江工业大学之江学院理学院学生谈话管理系统</div>
        <div class="flex flex-col md:flex-row">
            <div class="mt-8 lg:mt-16 mx-4 flex justify-center md:w-2/5 h-96">
                <div class="p-8 lg:p-12 rounded-xl shadow-xl mx-auto">
                    <div class="text-center text-2xl font-semibold mt-3 mb-6">登录</div>
                    <t-input size="large" label="账号" placeholder="账号" v-model="account" class="mt-12"></t-input>
                    <t-input size="large" label="密码" placeholder="密码" v-model="password" type="password" class="my-6"
                        @enter="loginRequest"></t-input>
                    <div class="flex justify-center">
                        <t-button @click="loginRequest" class="mt-4" :loading="loading" size="large">
                            登录
                        </t-button>
                    </div>
                </div>
            </div>
            <div class="lg:mx-20 lg:mt-20 mt-12 mx-12 lg:pt-20 pt-8 py-8 flex-wrap md:w-3/5">
                <p class="leading-relaxed font-semibold text-4xl text-transparent bg-clip-text bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500">世界上没有才能的人是没有的。问题在于教育者要去发现每一位学生的禀赋、兴趣、爱好和特长，为他们的表现和发展提供充分的条件和正确引导。</p>
                <p class="pt-8 text-3xl font-bold text-right text-stone-600">苏霍姆林斯基</p>
            </div>
        </div>
    </div>
</template>