<template>
    <v-container fluid v-if="pictures.length !== 0">

        <v-row align="center" justify="center" class="elevation-2 gallery-row" >
            <v-col cols="12">

                <p id="gallery" /> <!-- Just an anchor for the gallery -->

                <Swiper :slides-per-view="1"
                        :space-between="50"
                        :navigation="gallerySettings.arrowsEnabled"
                        :pagination="{ clickable: true, DynamicBullets: true }"
                        :modules="modules"
                        :centeredSlides="true"
                        :loop="slidesLoop"
                        grab-cursor >

                    <SwiperSlide v-for="item in pictures" :key="item.id" :virtualIndex="galleryIndex">

                        <a  class="site-anchor"
                            :href="item.news_id == null ? item.link : redirectOnClick"
                            @click="item.news_id == null ? emitNewsSearch(-1) : emitNewsSearch(item.news_id)" >
                            <v-img  :src="mediaUrl + item.picture" :alt="item.description"
                                    class="gallery-image" />
                        </a>

                    </SwiperSlide>

                </Swiper>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import SwiperCore, { Navigation, Pagination, A11y, Virtual } from "swiper";
    import { Swiper, SwiperSlide } from "swiper/vue";
    import 'swiper/css';
    import 'swiper/css/bundle';
    import "swiper/css/pagination";
    import $ from "jquery";

    SwiperCore.use([Navigation, Pagination, A11y, Virtual]);

    export default {
        name: 'LADIGallery',
        components: {
            Swiper,
            SwiperSlide
        },
        props: {
            'galleryTitle': {
                type: String,
                default: function () {
                    return 'None';
                }
            },
            'slidesLoop': {
                type: Boolean,
                default: function () {
                    return false;
                }
            },
            'redirectOnClick': {
                // Redirection when no link is present
                type: String,
                default: function () {
                    return '#gallery';
                }
            },
        },
        data: () => ({
            pictures: [],
            galleryId: 0,
            galleryIndex: 0,
            api_base_url: 'http://localhost/',
            picturesUrl: 'http://localhost/ladipictures/',
            galleriesUrl: 'http://localhost/ladigalleries/',
            mediaUrl: 'http://localhost/storage/',
            gallerySettings: {
                'arrowsEnabled': true,
            }
        }),
        setup() {
            return {
                modules: [Pagination],
            };
        },
        created() {
            this.emitter.on('updateGallery', (evt) => {
                if (isNaN(evt.id)){ return; }
                this.galleryId = evt.id;
                this.updateGallery();
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.picturesUrl = `${this.api_base_url}ladipictures/`;
            this.galleriesUrl = `${this.api_base_url}ladigalleries/`;
            this.gallerySettings.arrowsEnabled = !this.isTouchDevice();
            this.updateGallery();
        },
        unmounted() {},
        methods: {
            isTouchDevice() {
                return ('ontouchstart' in window) ||
                    (navigator.maxTouchPoints > 0) ||
                    (navigator.msMaxTouchPoints > 0);
            },
            emitNewsSearch(newsId) {
                this.emitter.emit('newsSearch', { 'id': parseInt(newsId) })
            },
            async updateGallery() {
                if (isNaN(this.galleryId) || (this.galleryId === 0 && this.galleryTitle === 'None')) { return; }
                const url = this.galleryId ? `${this.galleriesUrl}pictures/?id=${this.galleryId}` : `${this.picturesUrl}?keyword=${this.galleryTitle}`;
                $.ajax({
                    url: url,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.pictures = [];
                        response.forEach(picture => {
                            if (picture.link == null) { picture.link = '#gallery' }
                            this.pictures.push(picture);
                        });
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
        }
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

    .gallery-image{
        height: 600px;
    }

    .gallery-row {
        border-radius: 15px;
        margin-inline: 15px;
    }

</style>
