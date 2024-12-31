<script setup>
import { ref } from "vue";
import { CloudUploadIcon, DeleteIcon } from "tdesign-icons-vue-next";
import { MessagePlugin } from "tdesign-vue-next";
import axios from "../axios";

const uploadRef = ref();
const files = ref([]);
const progress = ref(0);

const requestMethod = (file) => {
    return new Promise((resolve) => {
        let formData = new FormData();
        formData.append("data", file.raw);
        file.percent = 0;
        axios.post("/admin/upload", formData).then((response) => {
            if (response.data.status == "ok") {
                file.percent = 100;
                resolve({ status: "success" });
                MessagePlugin.success("上传成功系统正在导入");
            } else {
                resolve({ status: "fail" });
                MessagePlugin.error("发生错误了，请检查文件");
            }
        });
    });
};

const upload = () => {
    uploadRef.value.uploadFiles();
};
</script>

<template>
    <p class="text-3xl font-bold px-10 pt-10">上传数据</p>
    <div class="my-5 px-10">
        <p>请上传学生的信息表，表内应含有表头。</p>
        <p>
            学号 姓名 性别 班级 政治面貌 民族 宗教信仰 手机 邮箱 QQ 寝室 床号
            联系人 户籍所在地 家庭联系人1 家庭联系人1电话 家庭联系人2
            家庭联系人2电话 居住地
        </p>
    </div>

    <p class="px-10 pt-5"></p>
    <div class="mt-8 p-8 flex flex-col items-center">
        <div>
            <t-space class="mb-6">
                <t-button variant="outline" theme="primary" @click="upload">
                    <template #icon>
                        <CloudUploadIcon class="w-1.5 h-1.5" />
                    </template>
                    点击上传
                </t-button>
                <t-button variant="outline" theme="danger" @click="files = []">
                    <template #icon>
                        <DeleteIcon class="w-1.5 h-1.5" />
                    </template>
                    清空
                </t-button>
            </t-space>
        </div>
        <t-upload
            :auto-upload="false"
            ref="uploadRef"
            v-model="files"
            draggable
            theme="custom"
            :request-method="requestMethod"
        >
            <template #dragContent="params">
                <ul v-if="files && files.length" class="p-0">
                    <li v-for="file in files" :key="file.name">
                        {{ file.name }}
                    </li>
                </ul>
                <div v-else>
                    <p v-if="params && params.dragActive">释放鼠标</p>
                    <div
                        class="text-center flex flex-col"
                        v-else-if="progress < 1"
                    >
                        <p class="text-lg">拖拽信息文件到此区域区域</p>
                        <p class="py-0.5">或</p>
                        <div class="mx-auto mt-1">
                            <t-button size="small">单击选择信息文件</t-button>
                        </div>
                    </div>
                </div>
                <div
                    class="mt-1 flex justify-center"
                    v-if="files && files.length"
                >
                    <t-button size="small">更换文件</t-button>
                </div>
            </template>
        </t-upload>
    </div>
</template>
