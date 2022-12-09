<template>
    <v-container fluid class="border border-dark view-container">

        <v-row align="center" justify="start">

            <v-col cols="auto">
                <RefreshIcon icon="mdi-book-outline" clickEvent="updateStories" :userLang="userLang" />
            </v-col>
            <v-col cols="auto">
                <v-select class="storySelector"
                          v-model="storySelectedType"
                          :items="storiesTypes"
                          item-title="text"
                          item-value="value"
                          label="Select"
                          persistent-hint
                          return-object
                          single-line
                          />
            </v-col>
            
        </v-row>
        <v-row align="center" justify="center">
            <v-col>

                <!-- Standard div with flex properties, waiting for v-flex implementation on vuetify 3 -->
                <div class="flex-div">

                    <StoryPreview v-for="item in stories"
                                  :key="item.id" :story="item" :userLang="userLang" />

                </div>

            </v-col>
        </v-row>

    </v-container>
</template>

<script>

    import StoryPreview from '@/components/StoryPreview.vue';
    import RefreshIcon from '@/components/RefreshIcon.vue';
    import $ from "jquery";

    export default {
        name: 'StoriesView',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                storiesUrl: 'http://localhost/ladistories/?attributes=light',
                stories: [],
                storiesTypes: [
                    { 'text': '', 'textEN': 'All', 'textIT': 'Tutto', 'value': '' },
                    { 'text': '', 'textEN': 'Stories', 'textIT': 'Storie', 'value': 'story_type' },
                    { 'text': '', 'textEN': 'Materials', 'textIT': 'Materiale', 'value': 'material_type' },
                ],
                storySelectedType: { 'text': '', 'textEN': 'All', 'textIT': 'Tutto', 'value': '' },
                userLang: this.$settings.userLang,
            }
        },
        components: {
            StoryPreview,
            RefreshIcon,
        },
        created(){
            this.emitter.on('updateStories', () => {
                this.updateStories();
            });
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
                this.updateLang();
            });
            this.$watch(() => this.$route.params, () => { 
            this.selectStoryType(); this.updateStories(); });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.storiesUrl = `${this.api_base_url}ladistories/?attributes=light`;
            this.updateLang();
            this.selectStoryType();
            this.updateStories();
        },
        watch: {
            storySelectedType() {
                this.updateStories();
                this.updateUrl();
            },
        },
        methods: {
            async updateStories() {
                const request_end = `,${this.storySelectedType.value}`;
                $.ajax({
                    url: this.storiesUrl + request_end,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.stories = [...response];
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
            updateLang() {
                this.storiesTypes.forEach((story, idx) => {
                    if (this.userLang === 'it') {
                        this.storiesTypes[idx].text = this.storiesTypes[idx].textIT;
                    } else {
                        this.storiesTypes[idx].text = this.storiesTypes[idx].textEN;
                    }
                });
            },
            updateUrl() {
                if (this.storySelectedType.value === 'story_type') {
                    this.$router.push({ name: 'stories', params: { storyType: 'story' } });
                } else if (this.storySelectedType.value === 'material_type') {
                    this.$router.push({ name: 'stories', params: { storyType: 'material' } });
                } else {
                    this.$router.push({ name: 'stories', params: {} });
                }
            },
            selectStoryType() {
                if (this.$route.params.storyType === '') { return }
                var apiType = 'story_type';
                if (this.$route.params.storyType === 'story') { apiType = 'story_type' }
                else if (this.$route.params.storyType === 'material') { apiType = 'material_type' }
                else { return }
                const storyType = this.storiesTypes.find(item => {
                    return item.value ===  apiType;
                });
                this.storySelectedType = storyType;
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .storySelector {
        margin-top: 25px;
    }

</style>