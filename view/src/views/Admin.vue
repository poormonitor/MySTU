<script setup>
import { IconFont } from 'tdesign-icons-vue-next';
const mngtPath = [
    { to: { name: "userAdmin" }, text: "用户管理", icon: "usergroup-add" },
    { to: { name: "uploadExcel" }, text: "上传数据", icon: "cloud-upload" }
]
</script>

<template>
    <div class="h-full flex flex-row divide-x">
        <div id="adminNavi" class="flex overflow-x-hidden basis-1/4 md:basis-1/6">
            <t-menu theme="light" :value="this.$route.name">
                <t-menu-item :value="path.to.name" :to="path.to" v-for="path in mngtPath">
                    {{ path.text }}
                    <template #icon>
                        <icon-font class="mt-1" :name="path.icon" />
                    </template>
                </t-menu-item>
            </t-menu>
        </div>
        <div class="basis-3/4 md:basis-5/6 adminHeight">
            <router-view></router-view>
        </div>
    </div>
</template>

<style>
.adminHeight {
    height: calc(100vh - 3.5rem)
}
</style>