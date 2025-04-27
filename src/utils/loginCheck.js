// loginCheck.js
import './api.js';
import {apiRequest} from "./api";
const LOGIN_PAGE = '/login'; // 登录页面路径

/**
 * 检查用户登录状态
 * @returns {Promise<boolean>} 返回用户是否已登录
 */
async function checkLogin() {
    try {
        const response = await apiRequest("/current", "POST", {});
        return response !== null;
    } catch (error) {
        console.error("Login check failed:", error);
        return false;
    }
}

/**
 * 初始化登录检查
 */
async function initLoginCheck() {
  const isLoggedIn = await checkLogin();
  if (!isLoggedIn) {
    alert("Please Login");
    window.location.href = LOGIN_PAGE;
  }
}

// 页面加载完成后执行检查
if (document.readyState === 'complete') {
  initLoginCheck();
} else {
  window.addEventListener('load', initLoginCheck);
}