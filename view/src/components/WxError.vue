<script setup>
import { useRoute, onMounted } from "vue-router";

const route = useRoute();

const info = {
    1: "您没有绑定，请联系辅导员/系统管理员",
    2: "数据传递错误，请重试",
};

onMounted(() => {
    if (route.params.error) {
        alert(info[route.params.error]);
    }
});
</script>

<template></template>
