import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

// 登录
export const login = (credentials) => {
  return api.post("/auth/login", credentials);
};

// 获取用户信息
export const getUserInfo = () => {
  return api.get("/users/me");
};

// 获取学习画像
export const getLearningProfile = (userId) => {
  return api.get(`/profiles/${userId}`);
};

// 更新学习画像
export const updateLearningProfile = (userId, profile) => {
  return api.put(`/profiles/${userId}`, profile);
};

// 发送AI对话消息
export const sendAIChatMessage = (message, context = {}) => {
  return api.post("/ai/chat", { message, context });
};

// 获取学习资源
export const getLearningResources = (filters = {}) => {
  return api.get("/resources", { params: filters });
};

// 生成学习路径
export const generateLearningPath = (profile) => {
  return api.post("/path/generate", profile);
};

// 管理后台 - 获取用户列表
export const getUsers = () => {
  return api.get("/admin/users");
};

// 管理后台 - 获取资源统计
export const getResourceStats = () => {
  return api.get("/admin/stats/resources");
};

export default api;
