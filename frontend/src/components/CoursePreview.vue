<template>
    <v-card elevation="2"
            class="border border-dark default-card" >

        <div class="text-overline mb-1"  v-if="staffs.professor.fullname != null">
                prof {{ staffs.professor.fullname }}
        </div>

        <v-img max-height="250px"
               alt="course.title"
               :src="mediaUrl + course.cover" />

        <v-card-title v-html="visibleTitle">
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
                visibleTitle: '',
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
            'descriptionMaxLen': {
                type: Number,
                default: function () {
                    return 200;
                }
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
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.userUrl = `${this.api_base_url}ladiuser/?id=`;
            this.updateCourseStaff();
            this.setDescription();
            this.truncateTitle();
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
                if (this.course.description.length > this.descriptionMaxLen) {
                    this.visibleDescription = this.course.description.slice(0, this.descriptionMaxLen) + '...';
                } else {
                    this.visibleDescription = this.course.description;
                }
            },
            truncateTitle() {
                if (this.checkHtml(this.course.title) != 0){
                    return;
                }
                if (this.course.title.length == this.titleOneLineMaxLen){
                    this.visibleTitle = this.course.title;
                    return;
                }
                let index;
                for (index = this.titleLineMaxLen; index < this.course.title.length; index+=this.titleLineMaxLen) {
                    this.visibleTitle += this.course.title.substring(index-this.titleLineMaxLen, index);
                    this.visibleTitle += '-<br>';
                }
                this.visibleTitle += this.course.title.substring(index-this.titleLineMaxLen, this.course.title.length);
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
            email(email) {
                window.open('mailto:' + email, '_self');
            }
        },
    }
</script>

<style scoped>

    @import "@/styles/main.css";

</style>