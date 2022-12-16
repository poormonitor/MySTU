<script setup>
import { ref, onMounted } from 'vue';
import { isNumber } from "lodash";
import { IconFont } from "tdesign-icons-vue-next"
import LogModule from "../components/LogModule.vue";
import InfoModule from "../components/InfoModule.vue";
import Search from "../components/Search.vue"
import axios from "../axios"

const currentClass = ref()
const currentStudent = ref()
const currentName = ref()
const classesData = ref()
const studentsData = ref()
const SearchVisible = ref(false)

const fetchClasses = () => {
    axios.get("/classes")
        .then((response) => {
            classesData.value = response.data.data.clsList
        })
}

const fetchStudents = (classid, callback, ...args) => {
    axios.get("/students", {
        params: {
            class: classid
        }
    })
        .then((response) => {
            studentsData.value = response.data.data.stuList
            currentClass.value = classid
            if (callback)
                callback(...args)
        })
}

const switchStudent = (studentid) => {
    currentStudent.value = studentid
    currentName.value = studentsData.value.find(item => item.id == studentid).name
    SearchVisible.value = false
}

const switchInfo = (cls, stu) => {
    let clsid = classesData.value.find(item => item.name == cls).id
    fetchStudents(clsid, switchStudent, stu)
}

onMounted(() => {
    fetchClasses()
})
</script>

<template>
    <div class="grid grid-cols-6 md:grid-cols-8 divide-x-2 h-full">
        <Search v-model:visible="SearchVisible" @updateInfo="switchInfo" @confirm="SearchVisible = false" />
        <div id="classOption" class="flex overflow-x-hidden overflow-y-auto">
            <t-menu theme="light" :value="currentClass" @change="fetchStudents">
                <t-menu-item v-for="cls in classesData" :value="cls.id"> {{ cls.name }} </t-menu-item>
            </t-menu>
        </div>
        <div id="studentOption" class="overflow-x-hidden overflow-y-auto" :class="{ 'flex': isNumber(currentClass) }">
            <t-menu theme="light" :value="currentStudent" v-if="isNumber(currentClass)" @change="switchStudent">
                <t-menu-item v-for="stu in studentsData" :value="stu.id"> {{ stu.name }} </t-menu-item>
            </t-menu>
            <div class="m-4" v-else>
                <t-skeleton theme="paragraph"></t-skeleton>
            </div>
        </div>
        <div id="studentInfo" class="col-span-4 md:col-span-6">
            <div v-if="currentStudent" class="h-full">
                <div id="basic" class="h-20 px-8 py-7">
                    <span class="text-3xl font-bold">{{ currentName }}</span>
                    <span class="ml-4 text-sm text-gray-500">{{ currentStudent }}</span>
                </div>
                <t-tabs :defaultValue="1">
                    <t-tab-panel :value="1">
                        <template #label>
                            <icon-font name="file-copy" class="mr-1" /> 基本信息
                        </template>
                        <InfoModule :student="currentStudent" />
                    </t-tab-panel>
                    <t-tab-panel :value="2" label="谈话记录">
                        <template #label>
                            <icon-font name="usergroup" class="mr-1" /> 谈话记录
                        </template>
                        <LogModule :student="currentStudent" />
                    </t-tab-panel>
                </t-tabs>
            </div>
            <div class="m-10" v-else>
                <t-skeleton theme="paragraph"></t-skeleton>
            </div>
        </div>
        <div class="z-10 cursor-pointer transition bg-whtie hover:bg-slate-100 shadow-lg hover:shadow-xl rounded-full absolute bottom-3 left-3 p-4 text-black"
            @click="SearchVisible = true">
            <div class="w-5 h-5 flex justify-items-center items-center">
                <icon-font class="text-black" size="large" name="search"></icon-font>
            </div>
        </div>
    </div>
</template>

<style>
.contentHeight {
    height: calc(100vh - 11.5rem)
}

.t-tabs__header {
    height: 3rem;
}

.t-default-menu .t-menu__item {
    height: auto;
}
</style>