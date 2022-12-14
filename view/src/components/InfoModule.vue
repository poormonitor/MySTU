<script setup>
import axios from "../axios"
import { ref, watch } from "vue";

const props = defineProps(["student"])
const loadingData = ref(false)
const studentInfo = ref()

const fetchStudentInfo = (student) => {
    loadingData.value = true
    axios.get("/student", {
        params: {
            student: student
        }
    })
        .then((response) => {
            studentInfo.value = response.data.data.studentInfo
            setTimeout(() => {
                loadingData.value = false
            }, import.meta.env.VITE_ANI_TIMEOUT)
        })
}

fetchStudentInfo(props.student)

watch(() => props.student, () => {
    fetchStudentInfo(props.student)
})

const infoMap = {
    "基本情况": {
        "sex": "性别",
        "cls": "班级",
        "party": "政治面貌",
        "people": "民族",
        "religion": "宗教信仰",
        "identity": "身份证号",
        "bank": "银行卡",
    },
    "联系方式": {
        "phone": "手机",
        "email": "邮箱",
        "qq": "QQ",
    },
    "校内信息": {
        "domitory": "寝室",
        "bed": "床号",
        "contact": "联系人",
    },
    "家庭情况": {
        "domicile": "户籍所在地",
        "residence": "居住地",
        "fcontact1": "家庭联系人1",
        "fcontact1phone": "家庭联系人1电话",
        "fcontact2": "家庭联系人2",
        "fcontact2phone": "家庭联系人2电话",
    },
    "其他": {
        "memo": "备注",
    }
}
</script>

<template>
    <div class="px-10 pt-3 pb-4 overflow-y-scroll contentHeight" v-if="!loadingData">
        <div class="mt-4 mb-8" v-for="k in Object.keys(infoMap)">
            <p class="font-semibold text-xl mb-3">{{ k }}</p>
            <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-x-4 gap-y-4">
                <div v-for="e in Object.keys(infoMap[k])">
                    <p>{{ infoMap[k][e] }}</p>
                    <p class="text-lg break-words">{{ studentInfo[e] }}</p>
                </div>
            </div>
        </div>
    </div>
    <t-loading class="mt-6 flex justify-center" text="加载中..." size="small" v-else></t-loading>
</template>