<script setup>
import axios from "../axios";
import { ref, watch } from "vue";
import { MessagePlugin } from "tdesign-vue-next";

const classes = ref([]);
const students = ref([]);
const currentClass = ref(null);
const currentStudent = ref(null);

const getClasses = () => {
    axios.get("/classes").then((response) => {
        if (response.data.status == "ok") {
            classes.value = response.data.data.clsList;
            currentClass.value = classes.value[0].id;
            getStudents();
        }
    });
};

const getStudents = () => {
    if (currentClass.value !== null) {
        axios.get("/students?class=" + currentClass.value).then((response) => {
            if (response.data.status == "ok") {
                students.value = response.data.data.stuList;
                students.value.unshift({ name: "全部", id: "all" });
                currentStudent.value = "all";
            }
        });
    }
};

const deleteInfo = () => {
    if (currentStudent.value === "all") {
        axios
            .post("/admin/delete/class", {
                cls: currentClass.value,
            })
            .then((response) => {
                if (response.data.status == "ok") {
                    getClasses();
                    MessagePlugin.success("删除成功");
                }
            });
    } else {
        axios
            .post("/admin/delete/student", {
                id: currentStudent.value,
            })
            .then((response) => {
                if (response.data.status == "ok") {
                    getStudents();
                    MessagePlugin.success("删除成功");
                }
            });
    }
};

getClasses();
watch(currentClass, getStudents);
</script>

<template>
    <p class="text-3xl font-bold px-10 pt-10">删除信息</p>
    <div class="mt-8 p-8 flex flex-col items-center">
        <t-form>
            <t-form-item label="班级" name="class">
                <t-select v-model="currentClass">
                    <t-option
                        :key="cls.id"
                        :value="cls.id"
                        :label="cls.name"
                        v-for="cls in classes"
                    />
                </t-select>
            </t-form-item>
            <t-form-item label="学生" name="student">
                <t-select v-model="currentStudent">
                    <t-option
                        :key="stu.id"
                        :value="stu.id"
                        :label="stu.name"
                        v-for="stu in students"
                    />
                </t-select>
            </t-form-item>
            <t-form-item>
                <t-popconfirm content="确认删除吗" @confirm="deleteInfo">
                    <t-button theme="danger" :disabled="!currentStudent">
                        删除
                    </t-button>
                </t-popconfirm>
            </t-form-item>
        </t-form>
    </div>
</template>
