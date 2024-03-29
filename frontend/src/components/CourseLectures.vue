<template>
    <v-container fluid v-if="courseId !== 0 && lectures.length !== 0">
        <v-row justify="center" allign="center" class="elevation-2 main-row" >

            <!-- Lectures -->
            <v-col>

                <RefreshIcon icon="mdi-book" clickEvent="updateLectures" :userLang="userLang" />
                <v-spacer />

                <v-carousel class="my-carousel"  
                            cycle hide-delimiter-background
                            :show-arrows="lecturesSettings.showArrows">

                    <v-carousel-item v-for="(group, index) in lecturesInBatches" :key="`G${index}`" height="475">

                        <div class="carousel-div" >

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
                                <v-card-actions>
                                    <v-row justify="center" allign="center">
                                        <v-col v-if="item.lecture_url === ''">
                                            <v-btn elevation="5" outlined
                                                   class="my-button"
                                                   :to="`${lectureUrl}${item.id}`" >
                                                <h4 v-if="userLang === 'it'">Apri</h4>
                                                <h4 v-else>Open</h4>
                                            </v-btn>
                                        </v-col>
                                        <v-col v-else>
                                            <v-btn elevation="5" outlined
                                                   class="my-button"
                                                   :href="item.lecture_url" >
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
        name: 'CourseLectures',
        components: {
            RefreshIcon,
        },
        props: {
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
            courseId: 0,
            lectures: [],
            lecturesInBatches: [],
            lecturesSettings: {
                'batchSize': 0,
                'showArrows': true,
                'showText': false,
                'oneLectureThreshold': 500,
                'twoLectureThreshold': 1100,
            },
            api_base_url: 'http://localhost/',
            lectureUrl: '/lecture/?id=',
            lecturesUrl: 'http://localhost/ladicourses/lectures/?',
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
            window.addEventListener("resize", this.adjustLecturesBatches);
            window.addEventListener("orientationchange", this.adjustLecturesBatches);
            this.emitter.on('updateLectures', () => {
                this.updateLectures();
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.lecturesUrl = `${this.api_base_url}ladicourses/lectures/?`;
            this.lecturesSettings.showArrows = !this.isTouchDevice();
            this.updateCourseId();
            this.updateLectures();
        },
        umounted() {
            window.removeEventListener("resize", this.adjustLecturesBatches);
            window.removeEventListener("orientationchange", this.adjustLecturesBatches);
        },
        methods: {
            isTouchDevice() {
                return ('ontouchstart' in window) ||
                    (navigator.maxTouchPoints > 0) ||
                    (navigator.msMaxTouchPoints > 0);
            },
            adjustLecturesBatches() {
                if (this.correctBatchSize !== this.lecturesSettings.batchSize || this.nestedLenght() !== this.lectures.length ) {
                    this.lecturesSettings.batchSize = this.correctBatchSize;
                    this.packLectures();
                }
            },
            packLectures() {
                let packedLectures = [];
                for (let i = 0; i < this.lectures.length; i += this.lecturesSettings.batchSize) {
                    const newPack = this.lectures.slice(i, i + this.lecturesSettings.batchSize);
                    packedLectures.push(newPack);
                }
                this.lecturesInBatches = [...packedLectures];
            },
            updateCourseId() {
                const url = new URL(window.location.href);
                const params = new URLSearchParams(url.search);
                this.courseId = parseInt(params.get('id'));
            },
            nestedLenght() {
                let counter = 0;
                this.lecturesInBatches.forEach((subArray) => {
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
            async updateLectures() {
                if (this.courseId <= 0) { return; }
                $.ajax({
                    url: this.lecturesUrl + `id=${this.courseId}`,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.lectures = [];
                        this.newsInEvidence = [];
                        response.forEach(lecture => {
                            lecture.visibleTitle = this.truncateTitle(lecture.title);
                            this.lectures.push(lecture);
                        });
                        this.adjustLecturesBatches();
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
