<template>
    <v-app>

        <!-- App bar -->
        <v-app-bar app prominent class="my-appbar"
                   v-if="!isLargeScreen" >

            <!-- Mobile + small desktop -->
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" class="nav-icon"/>
            <v-toolbar-title><h3 class="mobile-header-title">LADISPE</h3></v-toolbar-title>
            <v-img alt="POLITO LOGO" :src="logo" class="mobile-logo"/>
        </v-app-bar>

        <!-- Navigation drawer -->
        <v-navigation-drawer v-model="drawer" absolute bottom temporary>
            <v-list nav density="compact">
                <v-list-item    v-for="item in menu" 
                                :key="item.text" @click="mobileMenuClickEvent(item)" 
                                :prepend-icon="item.icon" :to="item.to" color="#007baa">
                    <v-list-item-title v-if="userLang === 'it'">
                        {{ item.textIT }}
                    </v-list-item-title>
                    <v-list-item-title v-else>
                        {{ item.text }}
                    </v-list-item-title>
                </v-list-item>
                <v-list-item prepend-icon="mdi-translate" @click="updateLang();">
                    <v-list-item-title v-if="userLang === 'it'">
                        English version
                    </v-list-item-title>
                    <v-list-item-title v-else>
                        Italian version
                    </v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <!-- Site structure -->
        <v-main>

            <!-- Large desktop -->
            <v-row justify="center" v-if="isLargeScreen">
                <Header />
            </v-row>

            <!-- MAIN (both mobile & desktop)-->
            <v-container fluid pa-0 class="content-box">

                <v-row justify="center">
                    <v-col cols="12" md="9" lg="9" xl="9" xxl="9" >
                        <router-view></router-view>
                    </v-col>

                    <!-- Desktop menu -->
                    <v-col cols="3" v-if="isLargeScreen">
                        <Menu :menu="menu" />
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
    import Header from '@/components/Header.vue';
    import Menu from '@/components/Menu.vue';
    import logo from '@/assets/logo_poli.svg';
    import { computed } from "vue";
    import { useDisplay } from "vuetify";

    export default {
        name: 'App',
        data: () => ({
            logo: logo,
            drawer: false,
            api_base_url: 'http://localhost/',
            userLang: navigator.language || navigator.userLanguage,
            menu: [
                // Use to attribute to map the router, staticUrl to link a web server resource
                {
                    text: 'Home',
                    textIT: 'Home',
                    to: '/',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-home',
                },
                {
                    text: 'Stories',
                    textIT: 'Storie',
                    to: '/stories/story',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-book',
                },
                {
                    text: 'Materials',
                    textIT: 'Materiale',
                    to: '/stories/material',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-desktop-classic ',
                },
                {
                    text: 'Courses',
                    textIT: 'Corsi',
                    to: '/courses',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-bookshelf',
                },
                {
                    text: 'Contacts',
                    textIT: 'Contatti',
                    to: '/contacts',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-card-account-phone',
                },
                {
                    text: 'Timetable',
                    textIT: 'Tabella orari',
                    to: '/pdf/timetable',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-timetable',
                },
                {
                    text: 'Forms',
                    textIT: 'Modulistica',
                    to: '/forms',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-file-pdf-box',
                },
                {
                    text: 'Rules',
                    textIT: 'Regolamento',
                    to: '/pdf/rules',
                    staticUrl: '',
                    isMediaUrl: false,
                    icon: 'mdi-clipboard-list',
                },
            ],
        }),
        components: {
            Header,
            Menu
        },
        setup(){
            const { name } = useDisplay();

            const isLargeScreen = computed(() => {
                switch (name.value) {
                    case 'xs': return false;
                    case 'sm': return false;
                    case 'md': return true;
                    case 'lg': return true;
                    case 'xl': return true;
                    case 'xxl': return true;
                }
                return false;
            })

            return { isLargeScreen };
        },
        created() {
            window.addEventListener("resize", this.checkDrawer);
            window.addEventListener("orientationchange", this.checkDrawer);
            window.addEventListener('gesturestart', this.preventZoom);
            window.addEventListener('gesturechange', this.preventZoom);
            window.addEventListener('gestureend', this.preventZoom);
            window.addEventListener('touchstart', this.preventZoom);
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.checkDrawer();
            this.prepareMediaUrls();
            this.userLang = this.$settings.userLang;
        },
        unmounted() {
            window.removeEventListener("resize", this.checkDrawer);
            window.removeEventListener("orientationchange", this.checkDrawer);
            window.removeEventListener('gesturestart', this.preventZoom);
            window.removeEventListener('gesturechange', this.preventZoom);
            window.removeEventListener('gestureend', this.preventZoom);
            window.removeEventListener('touchstart', this.preventZoom);
        },
        watch: {
            group() {
                this.drawer = false
            }
        },
        methods: {
            mobileMenuClickEvent(item)
            {
                if (item.staticUrl !== ''){
                    window.location.href = item.staticUrl;
                }
            },
            checkDrawer() {
                // Close the drawer if it is in the desktop layout
                if (this.isLargeScreen) {
                    this.drawer = false;
                } 
            },
            preventZoom(e) {
                // Mobile prevent zoom
                e.preventDefault();
                document.body.style.zoom = 1;
            },
            prepareMediaUrls(){
                this.menu.forEach((element, index) => {
                    if (element.isMediaUrl){
                        element.staticUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}${element.staticUrl}`;
                        this.menu[index] = element;
                    }
                });
            },
            updateLang() {
                const newUserLang = (this.userLang == 'en') ? 'it' : 'en';
                this.emitter.emit('updateLang', { 'lang': newUserLang });
                this.userLang = newUserLang;
                this.$settings.userLang = newUserLang;
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .content-box {
        background-color: white;
        padding-top: 35px;
    }

    .my-appbar {
        background-color: white;
    }

    .mobile-header-title {
        text-align: left;
        color: #003576;
    }

    .mobile-logo {
        height: 85%;
    }

    .nav-icon {
        background-color: #007baa;
        border-radius: 7%;
        color: white;
        width: 64px;
        height: 40px;
    }

</style>