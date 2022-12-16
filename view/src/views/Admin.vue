<script setup>
import { IconFont } from 'tdesign-icons-vue-next';
const mngtPath = [
    { to: { name: "userAdmin" }, text: "用户管理", icon: "usergroup-add" }
]
</script>

<template>
    <Header />
    <div class="pt-14 h-screen">
        <div id="adminNavi" class="flex overflow-x-hidden overflow-y-auto max-h-screen">
            <t-menu theme="light">
                <t-menu-item :to="path.to" v-for="path in mngtPath">
                    {{ path.text }}
                    <template #icon>
                        <icon-font class="mt-1" :name="path.icon" />
                    </template>
                </t-menu-item>
            </t-menu>
        </div>
    </div>
</template>