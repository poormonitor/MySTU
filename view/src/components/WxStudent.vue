<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "../axios";
import RecordModule from "./RecordModule.vue";

const router = useRouter();

const token = sessionStorage.getItem("access_token_mystu");
const role = sessionStorage.getItem("role_mystu");
if (!token || role !== "1") {
    router.push({ name: "wx-welcome" });
}

const currentStudent = ref(null);
const studentInfo = ref({ name: "", class: "" });

axios.get("/wx/info").then((response) => {
    currentStudent.value = response.data.data.id;
    studentInfo.value = response.data.data;
});
</script>

<template>
    <div v-if="currentStudent">
        <div class="px-10 pt-10">
            <p class="text-xl font-semibold mb-1">{{ studentInfo.name }}</p>
            <p>{{ studentInfo.class }}</p>
            <p>{{ currentStudent }}</p>
        </div>

        <div class="mt-1">
            <RecordModule :student="currentStudent" />
        </div>
    </div>
    <div class="mt-6 flex justify-center" v-else>
        <t-loading text="加载中..." size="small"></t-loading>
    </div>
</template>

<style scoped>
.contentHeight {
    height: auto;
}
</style>
