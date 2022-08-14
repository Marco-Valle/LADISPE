<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row align="center" justify="center">

            <v-col>
                <h1 align="center" class="story-title">{{ story.title }}</h1>
                <h3 align="center" v-if="story.author !== 'None'">
                    {{ story.author }}
                </h3>
            </v-col>

        </v-row>

        <v-row v-if="story.gallery !== 'None'"
               align="center" justify="center">
            <v-col>

                <Gallery    :galleryId="story.gallery" />

            </v-col>
        </v-row>

        <v-row align="center" justify="center">
            <v-col>

                <v-card elevation="2"
                        class="border border-dark story-card" >
                    <v-card-content>

                        <span class="story-span" v-html="story.html" />
                        <p v-if="story.quote !== 'None'"
                           class="story-quote">
                            {{ story.quote }}
                        </p>

                    </v-card-content>
                </v-card>
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
    import Gallery from '@/components/Gallery.vue';
    import $ from "jquery";

    export default {
        name: 'StoryView',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                storyUrl: 'http://localhost/ladistories/?id=',
                mediaUrl: 'http://localhost/storage/',
                story: {
                    'id': 0,
                    'gallery': 0,
                },
            }
        },
        components: {
            Gallery,
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.storyUrl = `${this.api_base_url}ladistories/?id=`
            this.updateStoryId();
            this.updateStory();
        },
        watch: {
            story: function () {
                this.emitGalleryUpdate(this.story.gallery);
            }
        },
        methods: {
            updateStoryId() {
                const url = new URL(window.location.href);
                const params = new URLSearchParams(url.search);
                this.story.id = params.get('id')
            },
            emitGalleryUpdate(galleryId) {
                if (!galleryId) { return; }
                this.emitter.emit('updateGallery', { 'id': parseInt(galleryId) });
            },
            async updateStory() {
                $.ajax({
                    url: this.storyUrl + this.story.id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.story = response;
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .story-quote {
        text-align: right;
        margin-top: 15px;
        font-family: 'Lucida Console', 'Courier New', monospace;
    }

</style>