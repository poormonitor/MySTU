<script setup>
import axios from "../axios";
import { ref, watch, shallowRef, onBeforeUnmount } from "vue";
import { Editor, Toolbar } from "@wangeditor/editor-for-vue";
import "@wangeditor/editor/dist/css/style.css";
import { MessagePlugin } from "tdesign-vue-next";

const props = defineProps(["student", "viewonly"]);
const viewonly = props.viewonly ?? false;
const loadingData = ref(false);
const studentInfo = ref();
const loadingSubmit = ref(false);
const memoEditing = ref(false);
const memoContent = ref();

const fetchStudentInfo = (student) => {
    loadingData.value = true;
    axios
        .get("/student", {
            params: {
                student: student,
            },
        })
        .then((response) => {
            studentInfo.value = response.data.data.studentInfo;
            memoContent.value = response.data.data.studentInfo.memo;
            loadingData.value = false;
        });
};

fetchStudentInfo(props.student);

watch(
    () => props.student,
    () => {
        fetchStudentInfo(props.student);
    }
);

const infoMap = {
    基本情况: {
        sex: "性别",
        cls: "班级",
        party: "政治面貌",
        people: "民族",
        religion: "宗教信仰",
    },
    联系方式: {
        phone: "手机",
        qq: "QQ",
        email: "邮箱",
    },
    校内信息: {
        domitory: "寝室",
        bed: "床号",
        contact: "联系人",
    },
    家庭情况: {
        fcontact1: "家庭联系人1",
        fcontact1phone: "家庭联系人1电话",
        fcontact2: "家庭联系人2",
        fcontact2phone: "家庭联系人2电话",
        residence: "居住地",
        domicile: "户籍所在地",
    },
};

const largeItem = ["email", "residence"];
const mediumItem = ["domicile"];

const editorRef = shallowRef();
const toolbarConfig = {};
const editorConfig = { placeholder: "请输入备注内容..." };
const handleCreated = (editor) => {
    editorRef.value = editor;
};

onBeforeUnmount(() => {
    const editor = editorRef.value;
    if (editor == null) return;
    editor.destroy();
});

const submitMemo = () => {
    axios
        .post("/memo", {
            memo: memoContent.value,
            id: props.student,
        })
        .then((response) => {
            if (response.data.status == "ok") {
                MessagePlugin.success("备忘提交成功");
                memoEditing.value = false;
            }
        });
};
</script>

<template>
    <div
        class="overflow-y-auto min-w-[400px] contentHeight"
        v-if="!loadingData"
    >
        <div
            class="grid grid-cols-5 lg:grid-cols-4 divide-y md:divide-x md:divide-y-0"
        >
            <div
                id="basicInfo"
                class="px-10 py-8 col-span-5 md:col-span-3 infoTab overflow-y-auto"
            >
                <div class="mb-7" v-for="k in Object.keys(infoMap)">
                    <p class="font-semibold text-xl mb-2">{{ k }}</p>
                    <div
                        class="grid grid-cols-2 lg:grid-cols-5 gap-x-4 gap-y-4"
                    >
                        <div
                            v-for="e in Object.keys(infoMap[k])"
                            :class="{
                                'md:col-span-3': largeItem.includes(e),
                                'md:col-span-2': mediumItem.includes(e),
                            }"
                        >
                            <p v-if="studentInfo[e]">{{ infoMap[k][e] }}</p>
                            <p class="text-lg break-words leading-tight">
                                {{ studentInfo[e] }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div
                id="memo"
                class="col-span-5 md:col-span-2 lg:col-span-1 infoTab overflow-x-hidden pb-6"
            >
                <div class="p-4 flex items-center gap-x-2">
                    <span class="font-semibold text-xl">备注</span>
                    <t-switch
                        v-model="memoEditing"
                        size="large"
                        v-if="!viewonly"
                    >
                        <template #label="slotProps">
                            {{ slotProps.value ? "修改" : "查看" }}
                        </template>
                    </t-switch>
                </div>
                <div id="memoEdit" v-if="memoEditing">
                    <Toolbar
                        :editor="editorRef"
                        :defaultConfig="toolbarConfig"
                        mode="simple"
                    />
                    <div class="h-[30vh]">
                        <Editor
                            class="overflow-hidden border-b"
                            v-model="memoContent"
                            :defaultConfig="editorConfig"
                            mode="simple"
                            @onCreated="handleCreated"
                        />
                    </div>
                    <div class="flex justify-center mt-6">
                        <t-button
                            @click="submitMemo"
                            :loading="loadingSubmit"
                            size="large"
                        >
                            提交
                        </t-button>
                    </div>
                </div>
                <div
                    class="px-4 pb-6 overflow-y-auto break-words"
                    v-else
                    v-html="memoContent"
                ></div>
            </div>
        </div>
    </div>
    <div class="mt-6 flex justify-center" v-else>
        <t-loading text="加载中..." size="small"></t-loading>
    </div>
</template>

<style>
@media (min-width: 768px) {
    .infoTab {
        height: calc(100vh - 11.5rem);
    }
}
</style>
