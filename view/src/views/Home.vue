<script setup>
import { ref, onMounted } from "vue";
import { isNumber } from "lodash";
import {
    FileCopyIcon,
    UsergroupIcon,
    SearchIcon,
} from "tdesign-icons-vue-next";
import LogModule from "../components/LogModule.vue";
import InfoModule from "../components/InfoModule.vue";
import EditStudent from "../components/EditStudent.vue";
import Search from "../components/Search.vue";
import BindStu from "../components/BindStu.vue";
import axios from "../axios";

const currentClass = ref();
const currentStudent = ref();
const currentData = ref();
const classesData = ref();
const studentsData = ref();
const imgItem = ref(false);
const currentTab = ref(1);
const SearchVisible = ref(false);
const userEditVisible = ref(false);
const userBindVisible = ref(false);
const studentRenderKey = ref(0);

const fetchClasses = (callback, ...args) => {
    axios.get("/classes").then((response) => {
        classesData.value = response.data.data.clsList;
        if (callback) callback(...args);
    });
};

const fetchStudents = (classid, callback, ...args) => {
    axios
        .get("/students", {
            params: {
                class: classid,
            },
        })
        .then((response) => {
            studentsData.value = response.data.data.stuList;
            currentClass.value = classid;
            if (callback) callback(...args);
        });
};

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

const switchStudent = (studentid) => {
    imgItem.value = false;
    currentStudent.value = studentid;
    currentData.value = studentsData.value.find((item) => item.id == studentid);
    SearchVisible.value = false;
    currentTab.value = 1;
    fetchStudentPic();
};

const switchInfo = (cls, stu) => {
    let clsid = classesData.value.find((item) => item.name == cls).id;
    fetchStudents(clsid, switchStudent, stu);
};

const updateCls = (cls) => {
    fetchClasses(() => {
        let clsid = classesData.value.find((item) => item.name == cls).id;
        fetchStudents(clsid);
    });
};

onMounted(() => {
    fetchClasses();
});
</script>

<template>
    <div class="flex divide-x-2 h-full overflow-x-auto overflow-y-hidden">
        <Search
            v-model:visible="SearchVisible"
            @updateInfo="switchInfo"
            @confirm="SearchVisible = false"
        />
        <EditStudent
            v-model="userEditVisible"
            :student="currentStudent"
            @after="updateCls"
            @refresh="studentRenderKey++"
            v-if="userEditVisible"
        />
        <BindStu :user="currentStudent" v-model="userBindVisible" />
        <div
            id="classOption"
            class="flex grow-0 shrink-0 w-48 overflow-x-hidden"
        >
            <t-menu theme="light" :value="currentClass" @change="fetchStudents">
                <t-menu-item v-for="cls in classesData" :value="cls.id">
                    <span> {{ cls.name }} </span>
                    <svg
                        width="4"
                        height="4"
                        class="inline ml-2"
                        v-if="cls.alert"
                    >
                        <circle cx="2" cy="2" r="2" fill="red" />
                    </svg>
                </t-menu-item>
            </t-menu>
        </div>
        <div
            id="studentOption"
            class="overflow-x-hidden grow-0 shrink-0 w-48"
            :class="{ flex: isNumber(currentClass) }"
        >
            <t-menu
                theme="light"
                :value="currentStudent"
                v-if="isNumber(currentClass)"
                @change="switchStudent"
            >
                <t-menu-item v-for="stu in studentsData" :value="stu.id">
                    <span>{{ stu.name }}</span>
                    <svg
                        width="4"
                        height="4"
                        class="inline ml-2"
                        v-if="stu.alert"
                    >
                        <circle cx="2" cy="2" r="2" fill="red" />
                    </svg>
                </t-menu-item>
            </t-menu>
            <div class="m-4" v-else>
                <t-skeleton theme="paragraph"></t-skeleton>
            </div>
        </div>
        <div id="studentInfo" class="flex-grow">
            <div v-if="currentStudent" class="h-full">
                <div id="basic" class="h-20 flex">
                    <div id="pic" class="ml-1 py-1">
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
                                <Transition>
                                    <div
                                        class="pl-4 self-end"
                                        v-if="currentTab == 1"
                                    >
                                        <t-button
                                            variant="dashed"
                                            size="small"
                                            @click="userEditVisible = true"
                                        >
                                            编辑
                                        </t-button>
                                    </div>
                                </Transition>
                                <Transition>
                                    <div
                                        class="pl-1 self-end"
                                        v-if="currentTab == 1"
                                    >
                                        <t-button
                                            variant="dashed"
                                            size="small"
                                            @click="userBindVisible = true"
                                        >
                                            {{
                                                currentData.weixin
                                                    ? "已绑定"
                                                    : "绑定微信"
                                            }}
                                        </t-button>
                                    </div>
                                </Transition>
                            </div>
                        </div>
                    </div>
                </div>
                <t-tabs v-model="currentTab">
                    <t-tab-panel :value="1">
                        <template #label>
                            <FileCopyIcon class="mr-1" /> 基本信息
                        </template>
                        <InfoModule
                            :student="currentStudent"
                            :key="studentRenderKey"
                        />
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
        </div>
        <div
            class="z-10 cursor-pointer border-2 border-gray-200 transition bg-white hover:bg-slate-100 shadow-lg hover:shadow-xl rounded-full absolute bottom-3 left-3 p-4 text-black"
            @click="SearchVisible = true"
        >
            <div class="flex justify-items-center items-center">
                <SearchIcon class="text-black" name="search"></SearchIcon>
            </div>
        </div>
    </div>
</template>

<style>
.red-dot {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4'%3E%3Ccircle cx='2' cy='2' r='2' fill='red' /%3E%3C/svg%3E");
}

.t-tabs__nav-container {
    margin-left: 6.5rem;
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

.v-enter-active,
.v-leave-active {
    transition: opacity 0.1s ease-in-out;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
