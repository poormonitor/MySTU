<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import {
    UsergroupAddIcon,
    CloudUploadIcon,
    ImageAddIcon,
    Delete1Icon,
    FormIcon,
    FileExportIcon,
    TipsDoubleIcon,
} from "tdesign-icons-vue-next";

const mngtPath = [
    { to: { name: "userAdmin" }, text: "用户管理", icon: UsergroupAddIcon },
    { to: { name: "uploadExcel" }, text: "上传数据", icon: CloudUploadIcon },
    { to: { name: "uploadRecord" }, text: "上传记录", icon: FormIcon },
    { to: { name: "uploadImage" }, text: "上传图片", icon: ImageAddIcon },
    { to: { name: "exportData" }, text: "导出数据", icon: FileExportIcon },
    { to: { name: "exportLog" }, text: "导出谈话记录", icon: TipsDoubleIcon },
    { to: { name: "delete" }, text: "删除信息", icon: Delete1Icon },
];
const route = useRoute();
const currentRoute = computed(() => route.name);
</script>

<template>
    <div class="h-full flex flex-row divide-x">
        <div id="adminNavi" class="flex overflow-x-hidden">
            <t-menu theme="light" :value="currentRoute">
                <t-menu-item
                    :value="path.to.name"
                    :to="path.to"
                    v-for="path in mngtPath"
                >
                    {{ path.text }}
                    <template #icon>
                        <Component class="!w-4 !h-4" :is="path.icon" />
                    </template>
                </t-menu-item>
            </t-menu>
        </div>
        <div class="basis-3/4 md:basis-5/6 overflow-x-auto adminHeight">
            <router-view></router-view>
        </div>
    </div>
</template>

<style>
.adminHeight {
    height: calc(100vh - 3.5rem);
}
</style>
