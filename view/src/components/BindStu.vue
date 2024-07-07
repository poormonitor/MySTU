<script setup>
import { watch, computed, ref } from "vue";
import QrcodeVue from "qrcode.vue";
import axios from "../axios";

const props = defineProps(["modelValue", "user"]);
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

watch(visible, (value) => {
    if (value) {
        let user = props.user;
        let role = 1;
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
            });
    }
});
</script>

<template>
    <t-dialog v-model:visible="visible" header="微信绑定">
        <div class="mt-6 flex justify-center" v-if="url">
            <qrcode-vue :value="url" :size="200" level="M"></qrcode-vue>
        </div>
        <div class="mt-6 flex justify-center" v-else>
            <t-loading text="正在登录..." size="small"></t-loading>
        </div>
    </t-dialog>
</template>
