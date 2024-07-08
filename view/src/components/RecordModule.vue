<script setup>
import axios from "../axios";
import { ref, watch, computed } from "vue";

const props = defineProps(["student"]);
const loadingData = ref(false);
const studentRecord = ref({
    score: [0, 0, 0],
    unqualified: [],
    attendance: [],
    award: [],
});

const fetchStudentInfo = (student) => {
    loadingData.value = true;
    axios
        .get("/record", {
            params: {
                student: student,
            },
        })
        .then((response) => {
            studentRecord.value = response.data.data.studentRecord;
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

const columns1 = [
    { colKey: "不及格学分", title: "不及格学分" },
    { colKey: "获得学分", title: "获得学分" },
    { colKey: "平均学分绩点", title: "平均学分绩点" },
];
const columns2 = [
    { colKey: "课程名称", title: "课程名称" },
    { colKey: "学分", title: "学分" },
    { colKey: "成绩", title: "成绩" },
    { colKey: "课程性质", title: "课程性质" },
];
const columns3 = [
    { colKey: "时间", title: "时间" },
    { colKey: "内容", title: "内容" },
    { colKey: "学时", title: "学时" },
];
const columns4 = [
    { colKey: "奖惩原因", title: "奖惩原因" },
    { colKey: "奖惩级别", title: "奖惩级别" },
];

const processData = (columns, data) => {
    if (!data) return [];
    return data.map((item, index) => {
        let obj = { index: index + 1 };
        let cols = columns.map((e) => e.colKey);
        for (let i = 0; i < cols.length; i++) {
            obj[cols[i]] = item[i];
        }
        return obj;
    });
};

const data1 = computed(() =>
    processData(columns1, [studentRecord.value.score])
);
const data2 = computed(() =>
    processData(columns2, studentRecord.value.unqualified)
);
const data3 = computed(() =>
    processData(columns3, studentRecord.value.attendance)
);
const data4 = computed(() => processData(columns4, studentRecord.value.award));
</script>

<template>
    <div class="mx-2 md:mx-8 my-4 md:my-10 flex flex-col gap-y-10">
        <p>更新时间: {{ studentRecord.last_update }}</p>
        <div>
            <h3 class="mx-2 mb-1 text-lg font-bold">学分信息</h3>
            <t-base-table row-key="index" :columns="columns1" :data="data1" />
        </div>
        <div>
            <h3 class="mx-2 mb-1 text-lg font-bold">不及格课程</h3>
            <t-base-table row-key="index" :columns="columns2" :data="data2" />
        </div>
        <div>
            <h3 class="mx-2 mb-1 text-lg font-bold">考勤记录</h3>
            <t-base-table row-key="index" :columns="columns3" :data="data3" />
        </div>
        <div>
            <h3 class="mx-2 mb-1 text-lg font-bold">奖惩记录</h3>
            <t-base-table row-key="index" :columns="columns4" :data="data4" />
        </div>
    </div>
</template>
