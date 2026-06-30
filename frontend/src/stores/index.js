import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    userInfo: null,
    token: null,
    learningProfile: {
      knowledgeBase: 0,
      cognitiveStyle: "",
      errorPreferences: [],
      learningGoals: "",
      preferredLearningStyle: "",
      currentProgress: 0,
    },
    chatHistory: [],
    learningResources: [],
    learningPath: [],
  }),
  actions: {
    setUserInfo(userInfo) {
      this.userInfo = userInfo;
      localStorage.setItem("userInfo", JSON.stringify(userInfo));
    },
    setToken(token) {
      this.token = token;
      localStorage.setItem("token", token);
    },
    setLearningProfile(profile) {
      this.learningProfile = profile;
      localStorage.setItem("learningProfile", JSON.stringify(profile));
    },
    addChatMessage(message) {
      this.chatHistory.push(message);
      localStorage.setItem("chatHistory", JSON.stringify(this.chatHistory));
    },
    clearChat() {
      this.chatHistory = [];
      localStorage.removeItem("chatHistory");
    },
    setLearningResources(resources) {
      this.learningResources = resources;
      localStorage.setItem("learningResources", JSON.stringify(resources));
    },
    setLearningPath(path) {
      this.learningPath = path;
      localStorage.setItem("learningPath", JSON.stringify(path));
    },
    logout() {
      this.userInfo = null;
      this.token = null;
      this.learningProfile = {
        knowledgeBase: 0,
        cognitiveStyle: "",
        errorPreferences: [],
        learningGoals: "",
        preferredLearningStyle: "",
        currentProgress: 0,
      };
      this.chatHistory = [];
      this.learningResources = [];
      this.learningPath = [];

      localStorage.removeItem("token");
      localStorage.removeItem("userInfo");
      localStorage.removeItem("learningProfile");
      localStorage.removeItem("chatHistory");
      localStorage.removeItem("learningResources");
      localStorage.removeItem("learningPath");
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.userInfo?.role === "admin",
    currentProfile: (state) => state.learningProfile,
  },
});
