<script setup>
import { reactive, computed, onMounted, ref } from "vue"
import { MessagePlugin } from 'tdesign-vue-next';
import axios from "../axios"

const props = defineProps(["modelValue", "student"])
const emit = defineEmits(["update:modelValue", "after", "refresh"])
const studentInfo = reactive({ data: null })
const originCls = ref(null)
const visible = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})
const infoMap = {
    "cls": "班级",
    "party": "政治面貌",
    "people": "民族",
    "religion": "宗教信仰",
    "phone": "手机",
    "qq": "QQ",
    "email": "邮箱",
    "domitory": "寝室",
    "bed": "床号",
    "contact": "联系人",
    "fcontact1": "家庭联系人1",
    "fcontact1phone": "家庭联系人1电话",
    "fcontact2": "家庭联系人2",
    "fcontact2phone": "家庭联系人2电话",
    "residence": "居住地",
    "domicile": "户籍所在地",
}

const fetchStudentInfo = (student) => {
    axios.get("/student", {
        params: {
            student: student
        }
    })
        .then((response) => {
            studentInfo.data = response.data.data.studentInfo
            for (var k in studentInfo.data) {
                if (!(k in infoMap) && k != "id") {
                    studentInfo.data[k] = undefined
                }
            }
            originCls.value = response.data.data.studentInfo.cls
        })
}

const submitRequest = () => {
    axios.post("/edit", studentInfo.data).then((response) => {
        if (response.data.status == "ok") {
            visible.value = false
            MessagePlugin.success("用户编辑成功")
            if (studentInfo.data.cls != originCls.value) {
                emit("after", studentInfo.data.cls)
            }
            emit("refresh")
        } else {
            MessagePlugin.error(response.data.data.msg)
        }
    })
}

onMounted(() => {
    fetchStudentInfo(props.student)
})

</script>

<template>
    <t-dialog width="600px" v-model:visible="visible" header="编辑信息" :confirm-on-enter="true"
        :on-confirm="submitRequest" placement="center">
        <t-form labelWidth="160px" :data="studentInfo.data" v-if="studentInfo.data">
            <div v-for="e in Object.keys(infoMap)" class="pt-1">
                <t-form-item :label="infoMap[e]" :name="e">
                    <t-input :placeholder="infoMap[e]" v-model="studentInfo.data[e]" type="text"></t-input>
                </t-form-item>
            </div>
        </t-form>
    </t-dialog>
</template>