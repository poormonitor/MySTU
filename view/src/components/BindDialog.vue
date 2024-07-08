<script setup>
import { watch, computed, ref } from "vue";
import QrcodeVue from "qrcode.vue";
import axios from "../axios";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["update:modelValue"]);
const visible = computed({
    get() {
        return props.modelValue;
    },
    set(value) {
        emit("update:modelValue", value);
    },
});

const url = ref("");
const attached = ref(false);

const fetchCode = () => {
    let user = sessionStorage.getItem("user_mystu");
    let role = 0;
    url.value = "";
    axios
        .get("/wx/create", {
            params: {
                attach: user,
                role: role,
            },
        })
        .then((response) => {
            let token = encodeURIComponent(response.data.data.token);
            url.value = location.origin + "/#/wx/bind?token=" + token;
            attached.value = response.data.data.attached;
        });
};

const unbind = () => {
    let user = sessionStorage.getItem("user_mystu");
    axios
        .get("/wx/unbind", {
            params: {
                attach: user,
                role: 0,
            },
        })
        .then(() => {
            fetchCode();
        });
};

watch(visible, (value) => {
    if (value) fetchCode();
});
</script>

<template>
    <t-dialog v-model:visible="visible" header="微信绑定">
        <div class="h-[300px] flex flex-col justify-center" v-if="url">
            <div class="text-center mb-3" v-if="attached">
                <span>该账户已绑定，</span>
                <span class="text-red-800 cursor-pointer" @click="unbind">
                    解绑
                </span>
            </div>
            <div class="flex justify-center">
                <qrcode-vue :value="url" :size="200" level="L"></qrcode-vue>
            </div>
            <div class="mt-4 flex justify-center">
                <t-button
                    size="small"
                    theme="default"
                    variant="outline"
                    @click="fetchCode"
                >
                    刷新
                </t-button>
            </div>
        </div>
        <div class="h-[300px] py-auto flex justify-center" v-else>
            <t-loading text="正在获取..." size="small"></t-loading>
        </div>
    </t-dialog>
</template>
