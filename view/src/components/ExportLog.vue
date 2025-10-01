<script setup>
import axios from "../axios";
import dayjs from "dayjs";
import { ref } from "vue";

const range = ref([]);
const loading = ref(false);

const presets = ref({
    最近半年: [dayjs().subtract(6, "month").toDate(), dayjs().toDate()],
    最近1个季度: [dayjs().subtract(3, "month").toDate(), dayjs().toDate()],
    今天: [dayjs().toDate(), dayjs().toDate()],
});

const base64toBlob = (base64) => {
    let bstr = atob(base64);
    let n = bstr.length;
    let u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: "application/octet-stream" });
};

const downloadInfo = () => {
    if (range.value.length === 0) {
        return;
    }
    loading.value = true;
    axios
        .post("/admin/download_log", {
            start_time: range.value[0],
            end_time: range.value[1],
        })
        .then((response) => {
            const blob = base64toBlob(response.data.data.file);
            const downloadLink = document.createElement("a");

            downloadLink.href = URL.createObjectURL(blob);
            downloadLink.setAttribute(
                "download",
                `MySTU_Export_Log_${new Date().getTime()}.xlsx`
            );

            downloadLink.click();

            URL.revokeObjectURL(downloadLink.href);
            loading.value = false;
        })
        .catch((error) => {
            loading.value = false;
        });
};
</script>

<template>
    <p class="text-3xl font-bold px-10 pt-10">导出谈话记录</p>
    <div class="my-5 px-10">
        <p>导出指定日期之间的学生谈话记录。</p>
    </div>

    <div class="mt-8 p-8 flex flex-col items-center">
        <t-form>
            <t-form-item label="起止时间" name="class">
                <t-date-range-picker v-model="range" :presets="presets" />
            </t-form-item>
            <t-form-item>
                <t-button
                    @click="downloadInfo"
                    :loading="loading"
                    :disabled="range.length !== 2"
                >
                    导出
                </t-button>
            </t-form-item>
        </t-form>
    </div>
</template>
