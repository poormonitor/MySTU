<script setup>
import { useRoute } from "vue-router";
import { onMounted } from "vue";

const route = useRoute();

const info = {
    1: "您没有绑定，请联系辅导员/系统管理员",
    2: "数据传递错误，请重试",
    3: "登录超时，请重试",
};

onMounted(() => {
    if (route.query.error) {
        alert(info[Number(route.query.error)]);
    }
});
</script>

<template></template>
