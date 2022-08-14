<template>
    <v-container fluid class="border border-dark view-container" >

            <v-row v-if="course.id >= 0 && course.title !== ''">
                <CourseInfos :course="course" :staffs="staffs" />
            </v-row>
            <v-row>
                <CourseLectures  :courseId="course.id" />
            </v-row>
            <v-row v-if="materials != null && (materials.length > 1 || (materials.length === 1 && materials[0].files.length !== 0))">
                <CourseMaterials :materials="materials"/>
            </v-row>

    </v-container>
</template>

<script>
    import CourseInfos from '@/components/CourseInfos.vue';
    import CourseMaterials from '@/components/CourseMaterials.vue';
    import CourseLectures from '@/components/CourseLectures.vue';
    import $ from "jquery";

    export default {
        name: 'CourseView',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                courseUrl: 'http://localhost/ladicourses/?id=',
                userUrl: 'http://localhost/ladiuser/?id=',
                materialUrl: 'http://localhost/ladicourses/materials/?id=',
                course: {
                    'id': 0,
                },
                staffs: {
                    'professor': {},
                    'firstAssistant': {},
                    'secondAssistant': {},
                },
                materials: [],
            }
        },
        components: {
            CourseInfos,
            CourseMaterials,
            CourseLectures,
        },
        created() {
            this.emitter.on('updateMaterial', () => {
                this.updateMaterial();
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.courseUrl = `${this.api_base_url}ladicourses/?id=`;
            this.userUrl = `${this.api_base_url}ladiuser/?id=`;
            this.materialUrl = `${this.api_base_url}ladicourses/materials/?id=`;
            this.updateCourseId();
            this.updateCourse();
            this.updateMaterial();
        },
        umounted() {},
        methods: {
            updateCourseId() {
                const url = new URL(window.location.href);
                const params = new URLSearchParams(url.search);
                this.course.id = parseInt(params.get('id'));
            },
            async updateCourse() {
                if (this.course.id <= 0) { return; }
                $.ajax({
                    url: this.courseUrl + this.course.id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.course = response;
                        if (this.course.id == null) {
                            this.course.id = 0;
                            return;
                        }
                        this.staffs.professor = { 'id': response.professor };
                        this.staffs.firstAssistant = response.first_assistant === 'None' ? null : { 'id': response.first_assistant };
                        this.staffs.secondAssistant = response.second_assistant === 'None' ? null : { 'id': response.second_assistant };
                        this.updateCourseStaff();
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
            async updateCourseStaff() {
                Object.keys(this.staffs).forEach(key => {
                    if (this.staffs[key] === null) { return; }
                    $.ajax({
                        url: this.userUrl + this.staffs[key].id,
                        type: "get",
                        dataType: "json",
                        success: (response) => {
                            this.staffs[key].fullname = `${response.name} ${response.surname}`;
                            this.staffs[key].email = response.email;
                        },
                        error: (jqXHR, textStatus, errorThrown) => {
                            this.staffs[key] = null;
                            console.error(textStatus, errorThrown);
                        }
                    });
                });
            },
            async updateMaterial() {
                if (this.course.id <= 0) { return; }
                $.ajax({
                    url: this.materialUrl + this.course.id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.materials = [...response];
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

