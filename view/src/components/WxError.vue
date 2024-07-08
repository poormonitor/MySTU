<script setup>
import { useRoute, useRouter } from "vue-router";
import { onMounted } from "vue";

const route = useRoute();
const router = useRouter();

const info = {
    1: "您没有绑定，请联系辅导员/系统管理员",
    2: "数据传递错误，请重试",
    3: "登录超时，请重试",
    4: "二维码已过期，请刷新页面",
    5: "学生不存在，请检查",
    6: "手机号错误，请重试",
    7: "该账户已被绑定，请联系辅导员",
    8: "您的微信已经绑定过了，请联系辅导员",
};

onMounted(() => {
    if (route.query.error) {
        alert(info[Number(route.query.error)]);

        switch (Number(route.query.error)) {
            case 1:
            case 5:
            case 6:
                router.push({ name: "wx-add" });
                break;
        }
    }
});
</script>

<template></template>
