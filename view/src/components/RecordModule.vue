<script setup>
import axios from "../axios";
import { ref, watch, computed } from "vue";

const props = defineProps(["student"]);
const loadingData = ref(false);
const studentRecord = ref({
    score: [],
    unqualified: [],
    attendance: [],
    award: [],
    activity: [],
    warning: "",
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
    { colKey: "专业排名", title: "专业排名" },
];
const columns2 = [
    { colKey: "课程名称", title: "课程名称", width: "40%" },
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
    { colKey: "奖惩时间", title: "奖惩时间" },
];
const columns5 = [
    { colKey: "活动名称", title: "活动名称" },
    { colKey: "活动时数", title: "活动时数" },
    { colKey: "活动日期", title: "活动日期" },
];

const processData = (columns, data) => {
    if (!data.length || !data[0].length) return [];
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
const data5 = computed(() =>
    processData(columns5, studentRecord.value.activity)
);
</script>

<template>
    <div class="contentHeight overflow-y-auto pb-12">
        <div class="px-10 pb-10 pt-6 md:pt-12" v-if="!loadingData">
            <p class="text-sm text-neutral-600 mb-8">
                更新时间: {{ studentRecord.last_update }}
            </p>
            <div class="flex flex-col gap-y-8 md:gap-y-12">
                <div v-if="studentRecord.warning.length">
                    <h3 class="mb-1 text-xl font-bold">提醒</h3>
                    <div class="text-lg text-red-600">
                        <p v-for="item in studentRecord.warning">
                            {{ item[0] }}
                        </p>
                    </div>
                </div>
                <div>
                    <h3 class="mb-1 text-lg font-bold">学分信息</h3>
                    <t-base-table
                        size="small"
                        row-key="index"
                        :columns="columns1"
                        :data="data1"
                    />
                </div>
                <div>
                    <h3 class="mb-1 text-lg font-bold">不及格课程</h3>
                    <t-base-table
                        size="small"
                        row-key="index"
                        :columns="columns2"
                        :data="data2"
                    />
                </div>
                <div>
                    <h3 class="mb-1 text-lg font-bold">考勤记录</h3>
                    <t-base-table
                        size="small"
                        row-key="index"
                        :columns="columns3"
                        :data="data3"
                    />
                </div>
                <div>
                    <h3 class="mb-1 text-lg font-bold">奖惩记录</h3>
                    <t-base-table
                        size="small"
                        row-key="index"
                        :columns="columns4"
                        :data="data4"
                    />
                </div>
                <div>
                    <h3 class="mb-1 text-lg font-bold">活动记录</h3>
                    <t-base-table
                        size="small"
                        row-key="index"
                        :columns="columns5"
                        :data="data5"
                    />
                </div>
            </div>
        </div>
        <div class="mt-6 flex justify-center" v-else>
            <t-loading text="加载中..." size="small"></t-loading>
        </div>
    </div>
</template>
