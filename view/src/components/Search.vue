<script setup>
import axios from "../axios";
import { ref } from "vue"

const searchKeyword = ref(null)
const searchResult = ref([])
const loading = ref(false)
const emit = defineEmits(["updateInfo"])

const updateResult = () => {
    if (searchKeyword.value == "") {
        return
    }
    loading.value = true
    axios.get("/search", {
        params: {
            s: searchKeyword.value
        }
    }).then(
        (response) => {
            if (response.data.status == "ok") {
                searchResult.value = response.data.data
            }
            setTimeout(() => {
                loading.value = false
            }, 200)
        }
    )
}

const gotoStudent = (cls, id) => {
    emit("updateInfo", cls, id)
}
</script>

<template>
    <t-dialog placement="center">
        <p class="text-xl font-bold text-black mb-3"> 搜索 </p>
        <t-input v-model="searchKeyword" size="large" clearable placeholder="按 Enter 搜索" @enter="updateResult" />
        <div class="mt-6">
            <div class="py-2 px-5 transition hover:bg-slate-200 rounded-2xl cursor-pointer select-none"
                v-for="result in searchResult" v-if="!loading" @click="gotoStudent(result.cls, result.id)">
                <p class="text-lg font-semibold text-black">{{ result.name }}</p>
                <p class="text-cyan-700 mt-0.5" v-html="result.content"></p>
            </div>
            <div class="mt-6 flex justify-center" v-else>
                <t-loading text="加载中..." size="small"></t-loading>
            </div>
        </div>
    </t-dialog>
</template>