<template>
    <v-card elevation="2"
            class="border border-dark default-card" >

        <v-img max-height="250px"
               alt="story.title"
               :src="mediaUrl + story.cover" />

        <v-card-title>
            {{ story.title }}
        </v-card-title>

        <v-card-subtitle v-if="story.author !== ''">
            {{ story.author }}
        </v-card-subtitle>

        <v-card-text v-if="story.preview !== ''" >
            <span>{{ story.preview }}</span>
        </v-card-text>

        <v-card-actions>
            <v-btn elevation="5" outlined
                   :to="`${storyUrl}${story.id}`"
                   class="my-button">
                <h4 v-if="userLang === 'it'">Apri</h4>
                <h4 v-else>Open</h4>
            </v-btn>
        </v-card-actions>

    </v-card>
    
</template>

<script>

    export default {
        name: 'StoryPreview',
        data: function () {
            return {
                storyUrl: 'story/?id=',
                mediaUrl: 'http://localhost/storage/',
                userLang: navigator.language || navigator.userLanguage,
            }
        },
        props: {
            'story': {
                type: Object,
                required: true
            },
        },
        mounted() {
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
        },
        methods: {},
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

</style>