<script setup>
import { ref } from "vue";
import { FileCopyIcon, UsergroupIcon } from "tdesign-icons-vue-next";
import { useRouter } from "vue-router";
import LogModule from "../components/LogModule.vue";
import InfoModule from "./InfoModule.vue";
import axios from "../axios";

const router = useRouter();

const token = sessionStorage.getItem("access_token_mystu");
const role = sessionStorage.getItem("role_mystu");
if (!token || role !== "0") {
    router.push({ name: "wx-welcome" });
}

const options = ref([]);

const studentsData = ref([]);
const currentStudent = ref(null);
const currentData = ref(null);
const currentTab = ref(1);
const imgItem = ref(false);
const studentRenderKey = ref(0);

axios.get("/classes").then((response) => {
    options.value = response.data.data.clsList.map((item) => {
        return {
            value: item.id,
            label: item.name,
            children: true,
        };
    });
});

const fetchStudentPic = () => {
    axios
        .get("/pic", {
            params: {
                id: currentStudent.value,
            },
        })
        .then((response) => {
            if (response.data.status == "ok") {
                let data = response.data.data;
                setTimeout(() => {
                    imgItem.value =
                        "data:image/" + data.format + ";base64, " + data.pic;
                }, 100);
            }
        });
};

const handleSelect = (studentid) => {
    imgItem.value = false;
    currentStudent.value = studentid;
    currentData.value = studentsData.value.find((item) => item.id == studentid);
    currentTab.value = 1;
    fetchStudentPic();
};

const load = (node) => {
    return new Promise((resolve) => {
        if (node.level === 0) {
            axios
                .get("/students", {
                    params: {
                        class: node.value,
                    },
                })
                .then((response) => {
                    studentsData.value = response.data.data.stuList;
                    let data = response.data.data.stuList.map((item) => {
                        return {
                            value: item.id,
                            label: item.name,
                        };
                    });
                    resolve(data);
                });
        }
    });
};
</script>

<template>
    <div class="py-2 px-6 h-14">
        <t-form>
            <t-form-item label="选择学生">
                <t-cascader
                    v-model="currentStudent"
                    :options="options"
                    :load="load"
                    @change="handleSelect"
                />
            </t-form-item>
        </t-form>
    </div>

    <div v-if="currentStudent">
        <div id="basic" class="h-20 flex">
            <div id="pic" class="ml-3 py-1">
                <t-image
                    class="h-[7.7rem] w-[5.5rem] self-end"
                    fit="cover"
                    :src="imgItem"
                    v-if="imgItem"
                />
                <div
                    class="h-[7.7rem] w-[5.5rem] bg-slate-200 blur-sm"
                    v-else
                ></div>
            </div>
            <div class="pl-6 flex">
                <div class="flex self-end flex-col">
                    <span class="text-3xl font-bold pb-1">
                        {{ currentData.name }}
                    </span>
                    <div class="flex items-center h-6">
                        <span class="text-sm text-gray-500">
                            {{ currentStudent }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
        <t-tabs v-model="currentTab">
            <t-tab-panel :value="1">
                <template #label>
                    <FileCopyIcon class="mr-1" /> 基本信息
                </template>
                <InfoModule :student="currentStudent" :key="studentRenderKey" />
            </t-tab-panel>
            <t-tab-panel :value="2" label="谈话记录">
                <template #label>
                    <UsergroupIcon name="usergroup" class="mr-1" />
                    谈话记录
                </template>
                <LogModule :student="currentStudent" />
            </t-tab-panel>
        </t-tabs>
    </div>
    <div class="m-10" v-else>
        <t-skeleton theme="paragraph"></t-skeleton>
    </div>
</template>

<style>
.t-tabs__nav-container {
    margin-left: 7rem;
}

.contentHeight {
    height: calc(100vh - 11.5rem);
}

.t-tabs__header {
    height: 3rem;
}

.t-default-menu .t-menu__item {
    height: auto;
}
</style>
