<template>
    <v-container fluid v-if="newsInEvidence.length !== 0">
        <v-row justify="center" align="center" class="elevation-4 main-row" >

            <!-- In evidence news -->
            <v-col>

                <RefreshIcon icon="mdi-newspaper" clickEvent="updateNewsInEvidence" :userLang="userLang" />
                <v-spacer />

                <v-carousel class="my-carousel"
                            cycle hide-delimiter-background
                            :show-arrows="newsSettings.showArrows" >
                    <v-carousel-item v-for="(group, index) in newsInBatches" :key="`G${index}`" height="450">

                        <div class="carousel-div">

                            <v-card v-for="item in group" :key="item.id"
                                    elevation="2"
                                    class="border border-dark default-card" >

                                <v-img height="250"
                                       alt="item.title"
                                       :src="mediaUrl + item.cover" />
                                <v-card-title v-html="item.visibleTitle">
                                </v-card-title>
                                <v-card-subtitle>
                                    {{ item.timestamp.split('T')[0] }}
                                </v-card-subtitle>
                                <v-card-text v-if="newsSettings.showText && item.text !== ''" >
                                    {{ item.text }}
                                </v-card-text>
                                <v-card-actions v-if="item.link != null || item.openButtonEnabled">
                                    <v-row justify="center" allign="center">
                                        <v-col v-if="item.link != null">
                                            <v-btn elevation="5" outlined class="my-button"
                                                   @click="openInNewTab(item.link)" >
                                                <h4>Link</h4>
                                            </v-btn>
                                        </v-col>
                                        <v-col v-if="item.openButtonEnabled">
                                            <v-btn elevation="5" outlined class="my-button"
                                                   @click="emitNewsSearch(item.id)" >
                                                <h4 v-if="userLang === 'it'">Apri</h4>
                                                <h4 v-else>Open</h4>
                                            </v-btn>
                                        </v-col>
                                    </v-row>
                                </v-card-actions>

                            </v-card>
                        </div>

                    </v-carousel-item>
                </v-carousel>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

    import RefreshIcon from '@/components/RefreshIcon.vue';
    import $ from "jquery";
    import { computed } from "vue";
    import { useDisplay } from "vuetify";

    export default {
        name: 'InEvidenceNews',
        components: {
            RefreshIcon,
        },
        props: {
            'textMaxLen': {
                type: Number,
                default: function () {
                    return 70;
                }
            },
            'titleLineMaxLen': {
                type: Number,
                default: function () {
                    return 22;
                }
            },
            'titleOneLineMaxLen': {
                type: Number,
                default: function () {
                    return 26;
                }
            },
            'userLang': {
                type: String,
                default: function () {
                    return 'it';
                }
            },
        },
        data: () => ({
            newsInEvidence: [],
            newsInBatches: [],
            newsSettings: {
                'batchSize': 0,
                'showArrows': true,
                'showText': false,
            },
            api_base_url: 'http://localhost/',
            newsInEvidenceUrl: 'http://localhost/ladinews/?attributes=in_evidence&sort=desc',
            mediaUrl: 'http://localhost/storage/',
        }),
        setup(){
            const { name } = useDisplay();

            const correctBatchSize = computed(() => {
                switch (name.value) {
                    case 'xs': return 1;
                    case 'sm': return 1;
                    case 'md': return 2;
                    case 'lg': return 3;
                    case 'xl': return 3;
                    case 'xxl': return 3;
                }
                return 1;
            })

            return { correctBatchSize };
        },
        created() {
            window.addEventListener("resize", this.adjustNewsBatches);
            window.addEventListener("orientationchange", this.adjustNewsBatches);
            this.emitter.on('updateNewsInEvidence', () => {
                this.updateNewsInEvidence();
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.newsInEvidenceUrl = `${this.api_base_url}ladinews/?attributes=in_evidence&sort=desc`;
            this.newsSettings.showArrows = !this.isTouchDevice();
            this.updateNewsInEvidence();
        },
        umounted() {
            window.removeEventListener("resize", this.adjustNewsBatches);
            window.removeEventListener("orientationchange", this.adjustNewsBatches);
        },
        methods: {
            isTouchDevice() {
                return ('ontouchstart' in window) ||
                    (navigator.maxTouchPoints > 0) ||
                    (navigator.msMaxTouchPoints > 0);
            },
            openInNewTab(url) {
                window.open(url, '_blank').focus();
            },
            scrollTo(id) {
                document.getElementById(id).scrollIntoView();
            },
            emitNewsSearch(newsId) {
                this.emitter.emit('newsSearch', { 'id': parseInt(newsId) });
                this.scrollTo("newsTable");
            },
            adjustNewsBatches() {
                if (this.correctBatchSize !== this.newsSettings.batchSize || this.nestedLenght() != this.newsInEvidence.length) {
                    this.newsSettings.batchSize = this.correctBatchSize;
                    this.packNews();
                }
            },
            packNews() {
                let packedNews = [];
                for (let i = 0; i < this.newsInEvidence.length; i += this.newsSettings.batchSize) {
                    const newPack = this.newsInEvidence.slice(i, i + this.newsSettings.batchSize);
                    packedNews.push(newPack);
                }
                this.newsInBatches = [...packedNews];
            },
            nestedLenght() {
                let counter = 0;
                this.newsInBatches.forEach((subArray) => {
                    counter += subArray.length;
                });
                return counter;
            },
            truncateTitle(title) {
                let visibleTitle='';
                if (this.checkHtml(title) != 0){
                    return visibleTitle;
                }
                if (title.length == this.titleOneLineMaxLen){
                    visibleTitle = title;
                    return visibleTitle;
                }
                let index;
                for (index = this.titleLineMaxLen; index < title.length; index+=this.titleLineMaxLen) {
                    visibleTitle += title.substring(index-this.titleLineMaxLen, index);
                    visibleTitle += '-<br>';
                }
                visibleTitle += title.substring(index-this.titleLineMaxLen, title.length);
                return visibleTitle;
            },
            checkHtml(string){
                if (
                    string.search('<') != -1 ||
                    string.search('>') != -1 || 
                    string.search('&lt;') != -1 ||
                    string.search('&gt;') != -1
                    ) {
                        return -1;
                    }
                return 0;
            },
            async updateNewsInEvidence() {
                $.ajax({
                    url: this.newsInEvidenceUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.newsInEvidence = [];
                        response.forEach(news => {
                            if (news.text.length > this.textMaxLen) {
                                news.text = news.text.slice(0, this.textMaxLen) + '...';
                            }
                            news.visibleTitle = this.truncateTitle(news.title);
                            news.openButtonEnabled = news.text.length > 0;
                            this.newsInEvidence.push(news);
                        });
                        this.adjustNewsBatches();
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            }
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

</style>