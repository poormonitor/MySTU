<script setup>
import { reactive, computed, onBeforeMount } from "vue"
import { MessagePlugin } from 'tdesign-vue-next';
import { LockOnIcon } from 'tdesign-icons-vue-next';
import axios from "../axios"
import sha256 from "crypto-js/sha256";

const props = defineProps(["modelValue", "user"])
const emit = defineEmits(["update:modelValue"])
const visible = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})

const passwd = reactive({
    passwd: ""
})

const validatePasswd = (val) => {
    if (/^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,32}$/.test(val)) {
        return { result: true, message: '符合要求', type: 'success' }
    } else {
        return { result: false, message: '密码必须包含字母和数字，长度在8-16位间', type: 'error' }
    }
}

const rules = {
    passwd: [{ validator: validatePasswd }],
}

const submitRequest = () => {
    if (!validatePasswd(passwd.passwd).result) {
        return
    }
    axios.post("/admin/passwd", {
        passwd: sha256(passwd.passwd).toString(),
        user: props.user
    }).then((response) => {
        if (response.data.status == "ok") {
            visible.value = false
            MessagePlugin.success("密码设置成功")
        }
    })
}

onBeforeMount(() => {
    passwd.passwd = ""
})

</script>

<template>
    <t-dialog v-model:visible="visible" header="密码修改" :confirm-on-enter="true" :on-confirm="submitRequest">
        <t-form :rules="rules" :data="passwd">
            <div class="m-8">
                <t-form-item label="新密码" name="passwd">
                    <t-input placeholder="新密码" v-model="passwd.passwd" type="password" autocomplete="new-password">
                        <template #prefix-icon>
                            <lock-on-icon />
                        </template>
                    </t-input>
                </t-form-item>
            </div>
        </t-form>
    </t-dialog>
</template>