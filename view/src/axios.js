import { MessagePlugin } from "tdesign-vue-next"
import { logOut } from "./func"
import axios from "axios"
import router from "./router"


const instance = axios.create({
    baseURL: "/api",
    timeout: 10000
});

instance.interceptors.request.use((config) => {
    let token = sessionStorage.getItem('access_token_mystu')
    if (token) {
        config.headers.Authorization = "Bearer " + token
    }
    return config
}, (error) => {
    return Promise.reject(error);
})

instance.interceptors.response.use((response) => {
    return response
}, (error) => {
    if (!error.response) {
        MessagePlugin.error("网络错误，请检查网络")
    } else if (error.response.status == 401) {
        logOut()
        MessagePlugin.error("您没有登录，请先登录")
        setTimeout(() => {
            router.push({ name: "login" })
            location.reload()
        }, 1000)
    } else {
        MessagePlugin.error("系统错误")
    }
    return Promise.reject(error);
})

export default instance