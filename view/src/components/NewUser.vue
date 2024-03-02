<script setup>
import { ref, computed, watch } from "vue";
import { MessagePlugin } from "tdesign-vue-next";
import {
    UserAvatarIcon,
    UserCircleIcon,
    LockOnIcon,
} from "tdesign-icons-vue-next";
import axios from "../axios";
import sha256 from "crypto-js/sha256";

const form = ref();
const props = defineProps(["modelValue", "user"]);
const emit = defineEmits(["update:modelValue", "submit"]);
const visible = computed({
    get() {
        return props.modelValue;
    },
    set(value) {
        emit("update:modelValue", value);
    },
});

watch(visible, () => {
    form.value.clearValidate();
});

const newUser = ref({ passwd: "", id: "", name: "", admin: false });

const validatePasswd = (val) => {
    if (/^(?=.*[0-9])(?=.*[a-zA-Z])[0-9A-Za-z~!@#$%^&*._?]{8,32}$/.test(val)) {
        return { result: true, message: "符合要求", type: "success" };
    } else {
        return {
            result: false,
            message: "密码必须包含字母和数字，长度在8-16位间",
            type: "error",
        };
    }
};

const rules = {
    user: [
        { required: true, message: "姓名必填", type: "error" },
        {
            min: 2,
            message: "至少需要两个字",
            type: "error",
            trigger: "blur",
        },
    ],
    id: [
        { required: true, message: "用户名必填", type: "error" },
        {
            min: 3,
            message: "至少需要两个字符",
            type: "error",
            trigger: "blur",
        },
    ],
    passwd: [{ validator: validatePasswd }],
};

const submitRequest = () => {
    if (!validatePasswd(newUser.value.passwd).result) {
        return;
    }
    axios
        .post("/admin/new", {
            passwd: sha256(newUser.value.passwd).toString(),
            user: newUser.value.user,
            admin: newUser.value.admin,
            id: newUser.value.id,
        })
        .then((response) => {
            if (response.data.status == "ok") {
                visible.value = false;
                emit(
                    "submit",
                    newUser.value.id,
                    newUser.value.user,
                    newUser.value.admin
                );
                newUser.value = { passwd: "", id: "", name: "", admin: false };
                MessagePlugin.success("用户添加成功");
            } else {
                MessagePlugin.error(response.data.data.msg);
            }
        });
};
</script>

<template>
    <t-dialog
        v-model:visible="visible"
        header="用户添加"
        :confirm-on-enter="true"
        :on-confirm="submitRequest"
    >
        <t-form :rules="rules" :data="newUser" ref="form">
            <div class="m-8">
                <t-form-item label="用户名" name="id">
                    <t-input
                        placeholder="用户名"
                        v-model="newUser.id"
                        type="text"
                        autocomplete="username"
                    >
                        <template #prefix-icon>
                            <UserAvatarIcon class="w-1.5 h-1.5" />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item label="姓名" name="user">
                    <t-input
                        placeholder="姓名"
                        v-model="newUser.user"
                        type="text"
                        autocomplete="nick"
                    >
                        <template #prefix-icon>
                            <UserCircleIcon class="w-1.5 h-1.5" />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item label="密码" name="passwd">
                    <t-input
                        placeholder="密码"
                        v-model="newUser.passwd"
                        type="password"
                        autocomplete="new-password"
                    >
                        <template #prefix-icon>
                            <LockOnIcon class="w-1.5 h-1.5" />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item label="管理员" name="admin">
                    <t-switch
                        v-model="newUser.admin"
                        size="large"
                        :label="['是', '否']"
                    ></t-switch>
                </t-form-item>
            </div>
        </t-form>
    </t-dialog>
</template>
