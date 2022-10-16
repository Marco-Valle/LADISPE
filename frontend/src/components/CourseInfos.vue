<template>
    <v-container fluid>

        <v-row v-if="course.id !== 0"
               justify="center" class="elevation-2 main-row">

            <v-col cols="4" v-if="isLargeScreen">
                <v-spacer />
                <v-img alt="course.title" class="course-img"
                       :src="mediaUrl + course.cover" max-height="250px" />
            </v-col>

            <v-col cols="12" md="8" lg="8" xl="8" xxl="8">

                <v-row align="center" justify="center" class="course-title-row" >
                    <v-col cols="12" md="8" lg="8" xl="8" xxl="8">
                        <h1 align="center">
                            {{ course.title }}
                        </h1>
                    </v-col>
                    <v-col>
                        <h2 :align="this.isLargeScreen ? 'left' : 'center'" 
                            :style="{   'margin-bottom': `${this.isLargeScreen ? '0px' : '10px'}`, 
                                        'margin-top': `${this.isLargeScreen ? '4px' : '0px'}`,
                                    }" >
                            ({{ course.course_code }})
                        </h2>
                    </v-col>
                </v-row>

                <v-row v-if="course.degree_course !== ''" class="course-degree-row" >
                    <v-col md-offset="1" lg-offset="1" xl-offset="1" xxl-offset="1">
                        <p class="course-degree-paragraph">
                            <span v-if="isLargeScreen && userLang === 'it'">
                                Corso di laurea:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            </span>
                            <span v-else-if="isLargeScreen">
                                Degree course:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                            </span>
                            <i>{{ course.degree_course }}</i>
                        </p>
                    </v-col>
                </v-row>

                <v-row align="center" justify="center">

                    <v-table    class="course-table"
                                :style="{   'margin-bottom': `${this.isLargeScreen ? '0px' : '10px'}`}" >
                        <tbody v-if="userLang === 'it'">
                            <tr v-for="(staff, index) in staffs" :key="index">
                                <td v-if="staff != undefined && isLargeScreen">
                                    <p v-if="index === 'professor'">Professore</p>
                                    <p v-else-if="index === 'firstAssistant'">Primo Assistente</p>
                                    <p v-else>Secondo Assistente</p>
                                </td>
                                <td v-if="staff != undefined">{{ staff.fullname }}</td>
                                <td v-if="staff != undefined">
                                    <a class="site-anchor" :href="`mailto:${ staff.email }`">{{ staff.email }}</a>
                                </td>
                            </tr>
                        </tbody>
                        <tbody v-else>
                            <tr v-for="(staff, index) in staffs" :key="index">
                                <td v-if="staff != undefined && isLargeScreen">
                                    <p v-if="index === 'professor'">Professor</p>
                                    <p v-else-if="index === 'firstAssistant'">First Assistant</p>
                                    <p v-else>Second Assistant</p>
                                </td>
                                <td v-if="staff != undefined">{{ staff.fullname }}</td>
                                <td v-if="staff != undefined">
                                    <a class="site-anchor" :href="`mailto:${ staff.email }`">{{ staff.email }}</a>
                                </td>
                            </tr>
                        </tbody>
                    </v-table>

                </v-row>
            
            </v-col>

        </v-row>

    </v-container>
</template>

<script>

    import { computed } from "vue";
    import { useDisplay } from "vuetify";

    export default {
        name: 'CourseInfos',
        components: {},
        props: {
            'course': {
                type: Object,
                required: true
            },
            'staffs': {
                type: Object,
                required: true
            },
            'userLang': {
                type: String,
                default: function () {
                    return 'it';
                }
            },
        },
        data: () => ({
            api_base_url: 'http://localhost/',
            mediaUrl: 'http://localhost/storage/',
        }),
        setup(){
            const { name } = useDisplay();

            const isLargeScreen = computed(() => {
                switch (name.value) {
                    case 'xs': return false;
                    case 'sm': return false;
                    case 'md': return true;
                    case 'lg': return true;
                    case 'xl': return true;
                    case 'xxl': return true;
                }
                return false;
            })

            return { isLargeScreen };
        },
        mounted(){
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`
        },
        methods: {}
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

    .course-degree-paragraph {
        margin-top: 1px;
        text-align: center
    }

    .course-degree-row {
        padding-left: 20px;
        margin-bottom: 15px;
    }

    .course-img {
        margin: 5%;
    }

    .course-table{
        background-color: inherit;
    }

    .course-title-row {
        margin-bottom: 20px;
    }

    table {
        border-collapse: separate;
        border-spacing: 50px 0;
    }

    td {
        padding: 10px 0;
    }

</style>