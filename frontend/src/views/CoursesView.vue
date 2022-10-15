<template>
    <v-container fluid class="border border-dark view-container" >

        <RefreshIcon icon="mdi-bookshelf" clickEvent="updateCourses" :userLang="userLang" />

        <!-- Standard div with flex properties, waiting for v-flex implementation on vuetify 3 -->
        <div class="flex-div">

            <CoursePreview v-for="item in courses" :key="item.course_code"
                          :course="item" :userLang="userLang" />

        </div>

    </v-container>
</template>

<script>

    import CoursePreview from '@/components/CoursePreview.vue';
    import RefreshIcon from '@/components/RefreshIcon.vue';
    import $ from "jquery";

    export default {
        name: 'CoursesView',
        data: function () {
            return {
                userLang: this.$settings.userLang,
                api_base_url: 'http://localhost/',
                coursesUrl: 'http://localhost/ladicourses/',
                courses: [],
            }
        },
        components: {
            CoursePreview,
            RefreshIcon,
        },
        created(){
            this.emitter.on('updateCourses', () => {
                this.updateCourses();
            });
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.coursesUrl = `${this.api_base_url}ladicourses/`;
            this.updateCourses();
        },
        methods: {
            async updateCourses() {
                $.ajax({
                    url: this.coursesUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.courses = [];
                        response.forEach(course => {
                            // Required for logged superusers, otherwise they may be able to see also hidden content
                            if (course.public === 'True' || course.public === true) {
                                this.courses.push(course);
                            }
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

<style scoped>

    @import "@/styles/main.css";

</style>