<script setup>
import { onMounted, ref, h, reactive } from "vue";
import { Switch, Button, MessagePlugin, Popconfirm } from "tdesign-vue-next";
import { IconFont } from "tdesign-icons-vue-next";
import PasswdEdit from "./PasswdEdit.vue";
import NewUser from "./NewUser.vue";
import axios from "../axios"

const data = ref([])
const userOperation = ref(null)
const passwdEditVisible = ref(false)
const newUserVisible = ref(false)

const columns = [
    { colKey: 'id', title: '用户名' },
    { colKey: 'name', title: '姓名' },
    { colKey: 'last_login', title: '上次登录' },
    {
        colKey: 'admin', title: '管理员?', cell: (_, { col, row }) => {
            return h(Switch,
                {
                    size: "large",
                    value: row.admin,
                    disabled: sessionStorage.getItem("user_mystu") == row.id,
                    label: ["是", "否"],
                    onChange(value) {
                        console.log(value)
                        switchAdmin(row.id, value)
                    }
                }
            )
        },
    },
    {
        colKey: 'passwd', title: '修改密码', cell: (_, { col, row }) => {
            return h(Button, {
                onClick() {
                    userOperation.value = row.id
                    passwdEditVisible.value = true
                },
                variant: "outline",
                size: "small"
            }, { icon: h(IconFont, { name: "lock-on" }), default: "修改密码" })
        }
    },
    {
        colKey: 'delete', title: '删除用户', cell: (_, { col, row }) => {
            return h(Popconfirm, {
                theme: "default",
                content: "确认删除用户吗？",
                onConfirm() {
                    deleteUser(row.id)
                },
            }, [h(Button, {
                variant: "outline",
                theme: "danger",
                size: "small"
            }, { icon: h(IconFont, { name: "delete" }), default: "删除用户" })])
        }
    },
]

const fetchUsers = () => {
    axios.get("/admin/user")
        .then((response) => {
            if (response.data.status == "ok") {
                data.value = response.data.data.users
                pagination.total = data.value.length
            }
        })
}

const switchAdmin = (id, val) => {
    let target = data.value.find(item => item.id == id)
    let origin = target.admin
    target.admin = val
    axios.post("/admin/admin", {
        id: id,
        val: val
    }).catch(() => {
        target.admin = origin
    }).then((response) => {
        if (response.data.status = "ok") {
            MessagePlugin.success("修改成功。")
        } else {
            target.admin = origin
        }
    })
}

const addUser = (id, name, admin) => {
    data.value.unshift({
        id: id,
        name: name,
        admin: admin
    })
}

const deleteUser = (id) => {
    axios.post("/admin/delete", {
        id: id
    }).then((response) => {
        if (response.data.status == "ok") {
            data.value.filter(item => item.id != id)
            MessagePlugin.success("删除成功。")
        }
    })
}

const pagination = reactive({
    defaultCurrent: 1,
    defaultPageSize: 5,
    total: 0,
});

onMounted(() => {
    fetchUsers()
})
</script>

<template>
    <PasswdEdit :user="userOperation" v-model="passwdEditVisible" />
    <NewUser v-model="newUserVisible" @submit="addUser" />
    <p class="text-3xl font-bold px-10 pt-10"> 用户管理 </p>
    <div class="px-12 pt-3">
        <div class="my-4">
            <t-button @click="newUserVisible = true">添加用户</t-button>
        </div>
        <t-table row-key="index" :data="data" :columns="columns" :stripe="true" :bordered="true" :hover="true"
            table-layout="auto" size="medium" :pagination="pagination" show-header="true" cell-empty-content="-">
        </t-table>
    </div>
</template>