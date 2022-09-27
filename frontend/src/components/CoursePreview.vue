<template>
    <v-card elevation="2"
            class="border border-dark default-card" >

        <div class="text-overline mb-1"  v-if="staffs.professor.fullname != null">
                prof {{ staffs.professor.fullname }}
        </div>

        <v-img max-height="250px"
               alt="course.title"
               :src="mediaUrl + course.cover" />

        <v-card-title>
            {{ course.title }}
        </v-card-title>

        <v-card-subtitle v-if="course.degree_course != null">
            {{ course.degree_course }}
        </v-card-subtitle>

        <v-card-text v-if="visibleDescription !== ''" >
            <span>{{ visibleDescription }}</span>
        </v-card-text>

        <v-card-actions>
            <v-row justify="center" align="center">
                <v-col>
                    <v-btn elevation="5" outlined class="my-button"
                           @click="email(staffs.professor.email)" >
                        <h4>Email</h4>
                    </v-btn>
                </v-col>
                <v-col>
                    <v-btn elevation="5" outlined class="my-button"
                           :to="`${courseUrl}${course.id}`" >
                        <h4 v-if="userLang === 'it'">Apri</h4>
                        <h4 v-else>Open</h4>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>

    </v-card>
    
</template>

<script>

    import $ from "jquery";

    export default {
        name: 'CoursePreview',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                courseUrl:  'course/?id=',
                userUrl: 'http://localhost/ladiuser/?id=',
                mediaUrl: 'http://localhost/storage/',
                visibleDescription: '',
                staffs: {
                    'professor': {
                        'id': this.course.professor_id,
                    },
                    'firstAssistant': this.course.first_assistant_id === 'None' ? null : { 'id': this.course.first_assistant_id },
                    'secondAssistant': this.course.second_assistant_id === 'None' ? null : { 'id': this.course.second_assistant_id },
                },
                userLang: navigator.language || navigator.userLanguage,
            }
        },
        props: {
            'course': {
                type: Object,
                required: true
            },
            'truncateAfterNChars': {
                type: Number,
                default: function () {
                    return 200;
                }
            },
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.userUrl = `${this.api_base_url}ladiuser/?id=`;
            this.updateCourseStaff();
            this.setDescription();
        },
        methods: {
            async updateCourseStaff() {
                Object.keys(this.staffs).forEach(key => {
                    if (this.staffs[key] === null) { return; }
                    $.ajax({
                        url: this.userUrl + this.staffs[key].id,
                        type: "get",
                        dataType: "json",
                        success: (response) => {
                            if (response.name == null || response.surname == null){
                                this.staffs[key].fullname = null;
                            } else {
                                this.staffs[key].fullname = `${response.name} ${response.surname}`;
                            }
                            this.staffs[key].email = response.email;
                        },
                        error: (jqXHR, textStatus, errorThrown) => {
                            this.staffs[key] = null;
                            console.error(textStatus, errorThrown);
                        }
                    });
                });
            },
            setDescription() {
                if (this.course.description.length > this.truncateAfterNChars) {
                    this.visibleDescription = this.course.description.slice(0, this.truncateAfterNChars) + '...';
                } else {
                    this.visibleDescription = this.course.description;
                }
            },
            email(email) {
                window.open('mailto:' + email, '_self');
            }
        },
    }
</script>

<style scoped>

    @import "@/styles/main.css";

</style>