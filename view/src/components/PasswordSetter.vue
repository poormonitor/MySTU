<script setup>
import { reactive, computed } from "vue"
import { MessagePlugin } from 'tdesign-vue-next';
import { LockOnIcon } from 'tdesign-icons-vue-next';
import axios from "../axios"
import sha256 from "crypto-js/sha256";

const props = defineProps(["modelValue"])
const emit = defineEmits(["update:modelValue"])
const visible = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:modelValue', value)
    }
})

const passwdSet = reactive({
    old: "",
    new: "",
    repeat: ""
})

const validatePasswd = (val) => {
    if (val == passwdSet.old) {
        return { result: false, message: '新旧密码一致', type: 'error' }
    } else if (/^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,32}$/.test(val)) {
        return { result: true, message: '符合要求', type: 'success' }
    } else {
        return { result: false, message: '密码必须包含字母和数字，长度在8-16位间', type: 'error' }
    }
}

const validateRepeat = (val) => {
    if (val == passwdSet.new) {
        return { result: true, message: '输入一致', type: 'success' }
    } else {
        return { result: false, message: '两次的输入不一致', type: 'error' }
    }
}

const rules = {
    new: [{ validator: validatePasswd }],
    repeat: [{ validator: validateRepeat }]
}

const submitRequest = () => {
    if (!validatePasswd(passwdSet.new).result || !validateRepeat(passwdSet.repeat).result) {
        return
    }
    axios.post("/passwd", {
        old: sha256(passwdSet.old).toString(),
        new: sha256(passwdSet.new).toString()
    }).then((response) => {
        if (response.data.status == "ok") {
            visible.value = false
            MessagePlugin.success("密码设置成功")
        } else if (response.data.status == "error") {
            MessagePlugin.error("原密码错误，请检查")
        }
    })
}

</script>

<template>
    <t-dialog v-model:visible="visible" header="密码修改" :confirm-on-enter="true" :on-confirm="submitRequest">
        <t-form :rules="rules" :data="passwdSet">
            <div class="m-8">
                <t-form-item label="原密码" name="old">
                    <t-input placeholder="原密码" v-model="passwdSet.old" type="password" autocomplete="current-password">
                        <template #prefix-icon>
                            <lock-on-icon />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item label="新密码" name="new">
                    <t-input placeholder="新密码" v-model="passwdSet.new" type="password" autocomplete="new-password">
                        <template #prefix-icon>
                            <lock-on-icon />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item label="重复新密码" name="repeat">
                    <t-input placeholder="重复新密码" v-model="passwdSet.repeat" type="password" @enter="submitRequest"
                        autocomplete="new-password">
                        <template #prefix-icon>
                            <lock-on-icon />
                        </template>
                    </t-input>
                </t-form-item>
            </div>
        </t-form>
    </t-dialog>
</template>