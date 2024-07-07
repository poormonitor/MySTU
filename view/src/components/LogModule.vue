<script setup>
import { watch, ref, shallowRef, onBeforeUnmount, reactive } from "vue";
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";
import { AddIcon } from "tdesign-icons-vue-next";
import axios from "../axios";
import "@wangeditor/editor/dist/css/style.css";

const props = defineProps(["student"]);

const loadingLogs = ref(false);
const loadingLog = ref(false);
const submitResult = ref();
const logsData = ref();
const logData = ref();
const logToSubmit = reactive({ title: "", content: "" });
const submitMessage = ref();
const editMode = ref(false);
const currentLog = ref();
const loadingSubmit = ref(false);

const fetchLogs = (student) => {
    loadingLogs.value = true;
    axios
        .get("/logs", {
            params: {
                student: student,
            },
        })
        .then((response) => {
            logsData.value = response.data.data.logList;
            setTimeout(() => {
                loadingLogs.value = false;
            }, import.meta.env.VITE_ANI_TIMEOUT);
        });
};

fetchLogs(props.student);

watch(
    () => props.student,
    () => {
        fetchLogs(props.student);
    }
);

const fetchLog = (logid) => {
    editMode.value = false;
    loadingLog.value = true;
    if (logid == "new") {
        logData.value = "";
        currentLog.value = logid;
        return;
    }
    axios
        .get("/record", {
            params: {
                id: logid,
            },
        })
        .then((response) => {
            logData.value = response.data.data.logInfo;
            currentLog.value = logid;
            setTimeout(() => {
                loadingLog.value = false;
            }, import.meta.env.VITE_ANI_TIMEOUT);
        });
};

const submitLog = () => {
    loadingSubmit.value = true;
    axios
        .post("/submit", {
            content: logToSubmit.content,
            title: logToSubmit.title,
            user: sessionStorage.getItem("user_mystu"),
            student: props.student,
        })
        .catch(() => {
            submitResult.value = "error";
            submitMessage.value = "提交失败，请检查网络";
        })
        .then((response) => {
            if (response.data.status == "ok") {
                submitResult.value = "success";
                submitMessage.value = "记录提交成功";
                fetchLogs(props.student);
                currentLog.value = response.data.data.id;
                editMode.value = false;
                fetchLog(currentLog.value);
            } else {
                submitResult.value = "error";
                submitMessage.value = response.data.error.msg;
            }
        })
        .finally(() => {
            loadingSubmit.value = false;
        });
};

const editorRef = shallowRef();
const toolbarConfig = {};
const editorConfig = { placeholder: "请输入谈话内容..." };
const handleCreated = (editor) => {
    editorRef.value = editor;
};

onBeforeUnmount(() => {
    const editor = editorRef.value;
    if (editor == null) return;
    editor.destroy();
});
</script>

<template>
    <div class="flex divide-x-2 min-w-[600px] contentHeight">
        <div
            class="flex h-full overflow-x-hidden col-span-1"
            v-if="!loadingLogs"
        >
            <t-menu theme="light" :value="currentLog" @change="fetchLog">
                <t-menu-item value="new" @click="editMode = true">
                    <template #icon>
                        <AddIcon class="w-1.5 h-1.5" />
                    </template>
                    <b>新增谈话记录</b>
                </t-menu-item>
                <t-menu-item
                    class="logItem"
                    v-for="log in logsData"
                    :value="log.id"
                >
                    <div class="leading-5 my-2">
                        <div class="text-xl font-bold">{{ log.title }}</div>
                        <div class="text-xs mt-1">{{ log.time }}</div>
                        <div class="text-xs">{{ log.user }}</div>
                    </div>
                </t-menu-item>
            </t-menu>
        </div>
        <t-loading
            class="mt-6 flex justify-center"
            text="加载中..."
            size="small"
            v-else
        ></t-loading>
        <div class="flex-grow">
            <div id="editArea" v-if="editMode || (currentLog && !loadingLog)">
                <div class="p-8" v-if="!editMode">
                    <p class="text-3xl font-bold">{{ logData.title }}</p>
                    <div class="mt-2 text-gray-500">
                        <span class="mr-5">填写人：{{ logData.user }}</span>
                        <span>填写时间：{{ logData.indate }}</span>
                    </div>
                    <p class="mt-6" v-html="logData.content"></p>
                </div>
                <div id="editorArea" v-else>
                    <div class="px-4 py-2">
                        <t-alert
                            :theme="submitResult"
                            :message="submitMessage"
                            v-if="submitResult"
                        />
                    </div>
                    <div class="p-4">
                        <t-input
                            placeholder="标题"
                            v-model="logToSubmit.title"
                        ></t-input>
                    </div>
                    <Toolbar
                        :editor="editorRef"
                        :defaultConfig="toolbarConfig"
                    />
                    <div class="h-[30vh]">
                        <Editor
                            class="overflow-hidden border-b"
                            v-model="logToSubmit.content"
                            :defaultConfig="editorConfig"
                            @onCreated="handleCreated"
                        />
                    </div>
                    <div class="flex justify-center mt-6">
                        <t-button
                            @click="submitLog"
                            :loading="loadingSubmit"
                            size="large"
                        >
                            提交
                        </t-button>
                    </div>
                </div>
            </div>
            <div class="mt-6 flex justify-center" v-else-if="loadingLog">
                <t-loading text="加载中..." size="small"></t-loading>
            </div>
            <div class="m-10" v-else>
                <t-skeleton theme="paragraph"></t-skeleton>
            </div>
        </div>
    </div>
</template>

<style scoped>
.logItem {
    height: auto !important;
}
</style>
