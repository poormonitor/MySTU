const logOut = () => {
    sessionStorage.removeItem("access_token_mystu");
    sessionStorage.removeItem("user_mystu");
    sessionStorage.removeItem("name_mystu");
    sessionStorage.removeItem("admin_mystu");
};

function isWeixin() {
    var ua = navigator.userAgent.toLowerCase();
    var isWXWork = ua.match(/wxwork/i) == "wxwork";
    var isWeixin = !isWXWork && ua.match(/MicroMessenger/i) == "micromessenger";
    return isWeixin;
}

export { logOut, isWeixin };
