<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row justify="center" allign="center" >

            <v-col v-if="error">
                <h1 v-if="userLang === 'it'" class="pdfLoadingError" >Errore durante il caricamento del PDF</h1>
                <h1 v-else class="pdfLoadingError" >Error occurred during the PDF loading</h1>
            </v-col>
            <v-col v-else>
                <vue-pdf-embed v-if="ready" :source="pdfUrl" @loading-failed="showError" />
            </v-col>

        </v-row>

    </v-container>
</template>

<script>

    import VuePdfEmbed from 'vue-pdf-embed';

    export default {
        name: 'PdfView',
        data: function () {
            return {
                mediaUrl: 'http://localhost/storage/',
                urlPrefix: 'uploads/',
                pdfName: 'rules',
                pdfUrl: '',
                ready: false,
                error: false,
                trustedNames: ['rules', 'timetable'],
                userLang: this.$settings.userLang,
            }
        },
        components: {
            VuePdfEmbed,
        },
        created() {
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
            });
        },
        mounted() {
            window.addEventListener("resize", this.updateReaderWidth);
            window.addEventListener("orientationchange", this.updateReaderWidth);
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.updatePdfUrl();
            this.ready = true;
        },
        umounted() {
            window.removeEventListener("resize", this.updateReaderWidth);
            window.removeEventListener("orientationchange", this.updateReaderWidth);
        },
        watch: {
            $route (){
                this.updatePdfUrl();
            }
        },
        methods: {
            updatePdfUrl() {
                if (this.$route.params.pdfName != undefined && this.trustedNames.includes(this.$route.params.pdfName)) {
                    this.pdfName = this.$route.params.pdfName;
                }
                this.pdfUrl = `${this.mediaUrl}${this.urlPrefix}${this.pdfName}.pdf`;
            },
            updateReaderWidth() {
                this.$router.go();
            },
            showError() {
                this.error = true;
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .pdfLoadingError{
        text-align: center;
        color: #003576;
    }

</style>

