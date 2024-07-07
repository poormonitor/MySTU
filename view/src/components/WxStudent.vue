<script setup>
const token = sessionStorage.getItem("token_mystu");
if (!token) {
    router.push({ name: "wx-welcome" });
}
</script>

<template>
    {{ token }}
</template>
