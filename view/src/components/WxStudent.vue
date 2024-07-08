<script setup>
import {useRouter} from "vue-router"

const router = useRouter();

const token = sessionStorage.getItem("access_token_mystu");
const role = sessionStorage.getItem("role_mystu");
if (!token || role !== "1") {
    router.push({ name: "wx-welcome" });
}
</script>

<template>
    {{ token }}
</template>
