<script setup>
import axios from "../axios";
import { ref } from "vue";

const classes = ref([]);
const currentClass = ref(null);
const loading = ref(false);

const getClasses = () => {
    axios.get("/classes").then((response) => {
        if (response.data.status == "ok") {
            let clsList = response.data.data.clsList.map((cls) => {
                return { id: cls.name, name: cls.name };
            });
            clsList.unshift({ name: "全部", id: "" });
            classes.value = clsList;
        }
    });
};

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
    loading.value = true;
    axios
        .post("/admin/download", { cls: currentClass.value })
        .then((response) => {
            const blob = base64toBlob(response.data.data.file);
            const downloadLink = document.createElement("a");

            downloadLink.href = URL.createObjectURL(blob);
            downloadLink.setAttribute(
                "download",
                `MySTU_Export_${new Date().getTime()}.xlsx`
            );

            downloadLink.click();

            URL.revokeObjectURL(downloadLink.href);
            loading.value = false;
        })
        .catch((error) => {
            console.error("Error downloading the file:", error);
            loading.value = false;
        });
};

getClasses();
</script>

<template>
    <p class="text-3xl font-bold px-10 pt-10">导出信息</p>
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
            <t-form-item>
                <t-button
                    @click="downloadInfo"
                    :loading="loading"
                    :disabled="currentClass === null"
                >
                    导出
                </t-button>
            </t-form-item>
        </t-form>
    </div>
</template>
