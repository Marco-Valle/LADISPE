<template>
    <v-card elevation="2" class="border border-dark default-card" >

        <v-img max-height="250"
               alt="staff.fullname"
               :src="mediaUrl + staff.cover" />

        <v-card-title>
            {{ staff.fullname }}
        </v-card-title>

        <v-card-subtitle v-if="staff.author !== ''">
            {{ staff.position }}
        </v-card-subtitle>

        <v-card-text>
            <p v-if="staff.phone !== ''">{{ staff.email }}</p>
            <p v-if="staff.phone !== ''">{{ staff.phone }}</p>
            <p v-if="staff.fax !== ''">{{ staff.fax }}</p>
        </v-card-text>

        <v-card-actions>
            <v-row justify="center" align="center">
                <v-col v-if="staff.email !== '' && staff.email != undefined">
                    <v-btn elevation="5" outlined
                           @click="email(staff.email)"
                           class="my-button" >
                        <h4>Email</h4>
                    </v-btn>
                </v-col>
                <v-col v-if="staff.phone !== '' && staff.phone != undefined">
                    <v-btn elevation="5" outlined
                           @click="call(staff.phone)"
                           class="my-button" >
                        <h4 v-if="userLang === 'it'">Chiama</h4>
                        <h4 v-else>Call</h4>
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-actions>

    </v-card>
    
</template>

<script>

    export default {
        name: 'StaffCard',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                mediaUrl: 'http://localhost/storage/',
                userLang: navigator.language || navigator.userLanguage,
            }
        },
        props: {
            'staff': {
                type: Object,
                required: true
            },
        },
        mounted(){
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`
        },
        methods: {
            call(phoneN) {
                window.open('tel:' + phoneN, '_self');
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