<script setup>
import { ref, computed } from "vue";
import {
    FileCopyIcon,
    SearchIcon,
    UsergroupIcon,
    AssignmentUserIcon,
} from "tdesign-icons-vue-next";
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

const SearchVisible = ref(false);

const studentsData = ref([]);
const classesData = ref([]);
const currentClass = ref(null);
const currentStudent = ref(null);
const currentData = ref(null);
const currentTab = ref(1);
const imgItem = ref(false);
const studentRenderKey = ref(0);

axios.get("/classes").then((response) => {
    classesData.value = response.data.data.clsList;
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
    currentData.value = studentsData.value.find((item) => item.id == studentid);
    currentTab.value = 1;
    fetchStudentPic();
};

const handleSelectClass = () => {
    fetchClass();
};

const fetchClass = async () => {
    return axios
        .get("/students", {
            params: {
                class: currentClass.value,
            },
        })
        .then((response) => {
            studentsData.value = response.data.data.stuList;
        });
};

const options = computed(() => {
    return studentsData.value.map((item) => {
        return {
            value: item.id,
            label: item.name,
        };
    });
});

const classesOptions = computed(() => {
    return classesData.value.map((item) => {
        return {
            value: item.id,
            label: item.name,
        };
    });
});

const switchInfo = (cls, id) => {
    let clsid = classesData.value.find((item) => item.name == cls).id;
    currentClass.value = clsid;
    fetchClass().then(() => {
        currentStudent.value = id;
        handleSelect(id);
    });
    SearchVisible.value = false;
};
</script>

<template>
    <div
        class="z-10 cursor-pointer border-2 border-gray-200 transition bg-white hover:bg-slate-100 shadow-lg hover:shadow-xl rounded-full fixed bottom-5 right-5 p-4 text-black"
        @click="SearchVisible = true"
    >
        <div class="flex justify-items-center items-center">
            <SearchIcon class="text-black" name="search"></SearchIcon>
        </div>
    </div>

    <Search
        v-model:visible="SearchVisible"
        @updateInfo="switchInfo"
        @confirm="SearchVisible = false"
    />

    <div class="py-2 px-6 h-14 flex justify-center">
        <div class="flex gap-x-3 items-center">
            <div class="text-sm text-neutral-700">选择学生</div>
            <t-select
                class="!w-32"
                :options="classesOptions"
                v-model="currentClass"
                @change="handleSelectClass"
            ></t-select>
            <t-select
                class="!w-24"
                v-model="currentStudent"
                :options="options"
                @change="handleSelect"
            ></t-select>
        </div>
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
                    <FileCopyIcon class="mr-1" />
                    基本信息
                </template>
                <InfoModule
                    :viewonly="true"
                    :student="currentStudent"
                    :key="studentRenderKey"
                />
            </t-tab-panel>
            <t-tab-panel :value="2" label="谈话记录">
                <template #label>
                    <UsergroupIcon class="mr-1" />
                    谈话记录
                </template>
                <LogModule :viewonly="true" :student="currentStudent" />
            </t-tab-panel>
            <t-tab-panel :value="3" label="个人记录">
                <template #label>
                    <AssignmentUserIcon class="mr-1" />
                    个人记录
                </template>
                <RecordModule :student="currentStudent" />
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

.t-tabs__nav-scroll {
    overflow-x: auto;
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
