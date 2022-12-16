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
const imgItem = ref(false)
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

const fetchStudentPic = () => {
    axios.get("/pic", {
        params: {
            id: currentStudent.value
        }
    }).then((response) => {
        if (response.data.status == "ok") {
            let data = response.data.data
            setTimeout(() => {
                imgItem.value = "data:image/" + data.format + ";base64, " + data.pic
            }, 100)
        }
    })
}

const switchStudent = (studentid) => {
    imgItem.value = false
    currentStudent.value = studentid
    currentName.value = studentsData.value.find(item => item.id == studentid).name
    SearchVisible.value = false
    fetchStudentPic()
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
                <div id="basic" class="h-20 flex">
                    <div id="pic" class="h-32 w-24 ml-1 p-0.5">
                        <t-image class="self-end" fit="cover" :src="imgItem" v-if="imgItem" />
                        <div class="h-full w-full bg-slate-100 blur-sm" v-else></div>
                    </div>
                    <div class="pb-4 pl-6 flex">
                        <span class="text-3xl font-bold self-end">{{ currentName }}</span>
                        <span class="pl-4 text-sm text-gray-500 self-end">{{ currentStudent }}</span>
                    </div>
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
.t-tabs__nav-container {
    margin-left: 7rem;
}

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