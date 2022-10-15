<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row align="center" justify="center">
            <v-col cols="auto">
                <RefreshIcon    icon="mdi-home" clickEvent="updateStories" 
                                :userLang="userLang" :tooltipEnabled="false"/>
            </v-col>
            <v-col>
                <h1 class="not-found-title" v-if="userLang === 'it'">Pagina non trovata</h1>
                <h1 class="not-found-title" v-else>Page not found</h1>
            </v-col>
        </v-row>
        <v-row align="center" justify="center">
            <v-col>
                <v-img alt="Error 404" :src="picture" class="not-found-picure"/>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>

    import picture from '@/assets/404.png';
    import RefreshIcon from '@/components/RefreshIcon.vue';

    export default {
        name: 'PageNotFound',
        data: function () {
            return {
                picture: picture,
                userLang: this.$settings.userLang,
            }
        },
        created() {
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
            });
        },
        components: {
            RefreshIcon,
        },
        methods: {}
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .not-found-title {
        text-align: center;
        margin-top: 10px;
    }

    .not-found-picure{
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 15px;
        max-width: 480px;
        border-radius: 10%;
    }

</style>