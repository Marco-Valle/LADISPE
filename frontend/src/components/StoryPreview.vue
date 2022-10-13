<template>
    <v-card elevation="2"
            class="border border-dark default-card" >

        <v-img max-height="250px"
               alt="story.title"
               :src="mediaUrl + story.cover" />

        <v-card-title v-html="visibleTitle">
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
                visibleTitle: '',
            }
        },
        props: {
            'story': {
                type: Object,
                required: true
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
        },
        mounted() {
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.truncateTitle();
        },
        methods: {
            
            truncateTitle() {
                if (this.checkHtml(this.story.title) != 0){
                    return;
                }
                if (this.story.title.length == this.titleOneLineMaxLen){
                    this.visibleTitle = this.story.title;
                    return;
                }
                let index;
                for (index = this.titleLineMaxLen; index < this.story.title.length; index+=this.titleLineMaxLen) {
                    this.visibleTitle += this.story.title.substring(index-this.titleLineMaxLen, index);
                    this.visibleTitle += '-<br>';
                }
                this.visibleTitle += this.story.title.substring(index-this.titleLineMaxLen, this.story.title.length);
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
        },
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

</style>