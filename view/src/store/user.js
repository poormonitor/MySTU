import { defineStore } from "pinia"

export const useUser = defineStore("user", {
    state: () => {
        return {
            user: "",
            name: "",
            admin: false
        }
    },
    actions: {
        login(id, name, admin) {
            this.user = id
            this.name = name,
                this.admin = admin
        }
    },
})