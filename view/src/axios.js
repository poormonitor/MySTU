import axios from "axios"
import router from "./router"
import swal from "sweetalert"

const instance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 1000
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
    sessionStorage.removeItem("access_token_mystu")
    sessionStorage.removeItem("user_mystu")
    if (error.response.status == 401) {
        swal("没有登录", "您没有登录，请先登录。", "info").then(() => {
            router.push({ name: "login" })
        })
    } else {
        swal("发生错误了", error.response.statusText, "error").then(() => {
            router.push({ name: "login" })
        })
    }
    return Promise.reject(error);
})

export default instance