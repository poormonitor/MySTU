<script setup>
import { ref } from "vue"
import { IconFont } from "tdesign-icons-vue-next";
import { MessagePlugin } from "tdesign-vue-next";
import axios from "../axios";

const uploadRef = ref()
const files = ref([])
const progress = ref(0)

const requestMethod = (file) => {
    return new Promise((resolve) => {
        let formData = new FormData()
        formData.append("data", file.raw)
        file.percent = 0;
        axios.post("/admin/upload", formData).then((response) => {
            if (response.data.status == "ok") {
                file.percent = 100
                resolve({ status: 'success' })
                MessagePlugin.success("上传成功！系统正在导入。")
            } else {
                resolve({ status: 'fail' })
                MessagePlugin.error("发生错误了，请检查文件。")
            }
        })
    });
};

const upload = () => {
    uploadRef.value.uploadFiles();
};
</script>

<template>
    <p class="text-3xl font-bold px-10 pt-10"> 上传数据 </p>
    <div class="mt-8 p-8 flex flex-col items-center">
        <div>
            <t-space class="mb-6">
                <t-button variant="outline" theme="primary" @click="upload">
                    <template #icon>
                        <icon-font name="cloud-upload" />
                    </template>
                    点击上传
                </t-button>
                <t-button variant="outline" theme="danger" @click="files = []">
                    <template #icon>
                        <icon-font name="delete" />
                    </template>
                    清空
                </t-button>
            </t-space>
        </div>
        <t-upload :auto-upload="false" ref="uploadRef" v-model="files" draggable theme="custom"
            :request-method="requestMethod">
            <template #dragContent="params">
                <ul v-if="files && files.length" class="p-0">
                    <li v-for="file in files" :key="file.name">{{ file.name }}</li>
                </ul>
                <div v-else>
                    <p v-if="params && params.dragActive">释放鼠标</p>
                    <div class="text-center flex flex-col" v-else-if="progress < 1">
                        <p class="text-lg">拖拽文件到此区域区域</p>
                        <p class="py-0.5">或</p>
                        <div class="mx-auto mt-1">
                            <t-button size="small">单击选择文件</t-button>
                        </div>
                    </div>
                </div>
                <div class="mt-1 flex justify-center" v-if="files && files.length">
                    <t-button size="small">更换文件</t-button>
                </div>
            </template>
        </t-upload>
    </div>
</template>