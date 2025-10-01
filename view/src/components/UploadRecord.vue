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
        axios.post("/admin/upload_record", formData).then((response) => {
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
    <p class="text-3xl font-bold px-10 pt-10">上传记录</p>
    <div class="my-5 px-10">
        <p>请上传学生的信息记录表，系统自动判断数据类型。</p>
        <p>数据格式：</p>
        <p>学分信息 表头：学号 不及格学分 获得学分 平均学分绩点 专业排名</p>
        <p>不及格课程 表头：学号 课程名称 学分 成绩 课程性质</p>
        <p>考勤记录 表头：学号 时间 内容 学时</p>
        <p>奖惩记录 表头：学号 奖惩原因 奖惩级别 奖惩时间</p>
        <p>活动记录 表头：学号 活动名称 活动时数 活动日期</p>
        <p>提醒 表头：学号 提醒</p>
    </div>

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
                        <p class="text-lg">拖拽记录文件到此区域区域</p>
                        <p class="py-0.5">或</p>
                        <div class="mx-auto mt-1">
                            <t-button size="small">单击选择记录文件</t-button>
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
