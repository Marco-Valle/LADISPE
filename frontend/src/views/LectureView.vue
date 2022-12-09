<template>
    <v-container fluid class="border border-dark view-container"
                 v-if="lecture.id >= 0 && lecture.title != null" >

        <v-row align="center" justify="center">
            <v-col>
                <h1 align="center" class="story-title">{{ lecture.title }}</h1>
                <h3 align="center" v-if="lecture.course !== 0">{{ course.title }} {{ course.course_code }}</h3>
            </v-col>

        </v-row>

        <v-row align="center" justify="center">
            <v-col>

                <v-card elevation="2" class="border border-dark story-card" >
                    <span class="story-span" v-html="lecture.html" />
                </v-card>

            </v-col>
        </v-row>

        <br />
        <h4 align="right" v-if="lecture.author !== 'None'">
            {{ lecture.author }}
        </h4>

    </v-container>
</template>

<script>
    import $ from "jquery";

    export default {
        name: 'LectureView',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                lectureUrl: 'http://localhost/ladilectures/?id=',
                courseUrl: 'http://localhost/ladicourses/?id=',
                mediaUrl: 'http://localhost/storage/',
                lecture: {
                    'id': 0,
                },
                course: {
                    'id': 0
                },
            }
        },
        components: {},
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.lectureUrl = `${this.api_base_url}ladilectures/?id=`;
            this.courseUrl = `${this.api_base_url}ladicourses/?id=`;
            this.updateLectureId();
            this.updateLecture();
        },
        methods: {
            updateLectureId() {
                const url = new URL(window.location.href);
                const params = new URLSearchParams(url.search);
                this.lecture.id = params.get('id')
            },
            async updateLecture() {
                if (this.lecture.id <= 0) { return; }
                $.ajax({
                    url: this.lectureUrl + this.lecture.id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.lecture = response;
                        this.updateCourse();
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
            async updateCourse() {
                if (this.lecture.course <= 0) { return; }
                $.ajax({
                    url: this.courseUrl + this.lecture.course,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.course = response;
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
    @import "@/styles/code.css";

</style>