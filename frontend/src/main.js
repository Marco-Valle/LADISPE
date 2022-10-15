import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import mitt from 'mitt'

loadFonts()

const app = createApp(App)
const emitter = mitt()

// Site settings
app.config.globalProperties.$settings = { 
    'userLang': navigator.language || navigator.userLanguage,
};

// Allow to use a custom base_url for the api
if (process.env.VUE_APP_URL != undefined && process.env.VUE_APP_URL !== ''){
    app.config.globalProperties.$base_url = `${process.env.VUE_APP_URL}/`;
} else {
    app.config.globalProperties.$base_url = `${window.location.origin}/`;
}
app.config.globalProperties.$api_base_url = app.config.globalProperties.$base_url;
if (process.env.VUE_APP_API_ENTRYPOINT != undefined && process.env.VUE_APP_API_ENTRYPOINT !== ''){
    app.config.globalProperties.$api_base_url +=  process.env.VUE_APP_API_ENTRYPOINT;
}

app.use(router)
app.use(vuetify)
app.config.globalProperties.emitter = emitter
app.mount('#app')