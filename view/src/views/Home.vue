<script setup>
import axios from "../axios"
import { ref, onActivated } from 'vue';
import { isNumber } from "lodash";
import LogModule from "../components/LogModule.vue";
import InfoModule from "../components/InfoModule.vue";

const currentClass = ref()
const currentStudent = ref()
const currentName = ref()
const classesData = ref()
const studentsData = ref()

const fetchClasses = () => {
    axios.get("/classes")
        .then((response) => {
            classesData.value = response.data.data.clsList
        })
}

const fetchStudents = (classid) => {
    axios.get("/students", {
        params: {
            class: classid
        }
    })
        .then((response) => {
            studentsData.value = response.data.data.stuList
            currentClass.value = classid
        })
}

const switchStudent = (studentid) => {
    currentStudent.value = studentid
    currentName.value = studentsData.value.find(item => item.id == studentid).name
}

onActivated(() => {
    fetchClasses()
})
</script>

<template>
    <div class="bg-gradient-to-r from-cyan-500 to-blue-500 px-6 py-3 absolute h-14 w-full">
        <span class="text-xl text-white font-semibold">浙江工业大学之江学院理学院学生谈话管理系统</span>
    </div>
    <div class="grid grid-cols-8 divide-x-2 pt-14 h-screen">
        <div id="classOption" class="overflow-x-hidden overflow-y-auto max-h-screen">
            <t-menu theme="light" :value="currentClass" @change="fetchStudents">
                <t-menu-item v-for="cls in classesData" :value="cls.id"> {{ cls.name }} </t-menu-item>
            </t-menu>
        </div>
        <div id="studentOption" class="overflow-x-hidden overflow-y-auto max-h-screen">
            <t-menu theme="light" :value="currentStudent" v-if="isNumber(currentClass)" @change="switchStudent">
                <t-menu-item v-for="stu in studentsData" :value="stu.id"> {{ stu.name }} </t-menu-item>
            </t-menu>
            <t-skeleton theme="paragraph" class="m-4" v-else></t-skeleton>
        </div>
        <div id="studentInfo" class="col-span-6">
            <div v-if="currentStudent" class="h-full">
                <div id="basic" class="h-16 px-6 py-4">
                    <span class="text-3xl font-bold">{{ currentName }}</span>
                    <span class="ml-4 text-sm text-gray-500">{{ currentStudent }}</span>
                </div>
                <t-tabs :defaultValue="1">
                    <t-tab-panel :value="1" label="基本信息">
                        <InfoModule :student="currentStudent" />
                    </t-tab-panel>
                    <t-tab-panel :value="2" label="谈话记录">
                        <LogModule :student="currentStudent" />
                    </t-tab-panel>
                </t-tabs>
            </div>
            <t-skeleton theme="paragraph" class="m-10" v-else></t-skeleton>
        </div>
    </div>
</template>

<style>
.contentHeight {
    height: calc(100vh - 10.5rem)
}

.t-tabs__header {
    height: 3rem;
}

.t-default-menu .t-menu__item {
    height: auto;
}
</style>