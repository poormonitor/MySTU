const logOut = () => {
    sessionStorage.removeItem("access_token_mystu")
    sessionStorage.removeItem("user_mystu")
    sessionStorage(removeItem("name_mystu"))
    sessionStorage(removeItem("admin_mystu"))
}

export { logOut }