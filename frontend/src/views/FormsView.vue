<template>
    <v-container fluid class="border border-dark view-container" >

        <v-icon size="x-large" @click="updateForms()">mdi-file-pdf-box</v-icon>
        <v-row align="center" justify="center">
            <v-col cols="12" sm="10" md="8" lg="6" xl="6" xxl="6">

                <v-list class="forms-list" v-if="forms.length !== 0">

                    <v-list-subheader>FILES</v-list-subheader>

                    <v-list-item    rounded="shaped"
                                    v-for="item in forms" :key="item.id">

                        <template v-slot:prepend>
                            <v-icon icon="mdi-file-pdf-box"></v-icon>
                        </template>
                        <a :href="mediaUrl + item.file" target="_blank">   
                            <v-list-item-title>
                                {{ item.title }}
                            </v-list-item-title>
                        </a>

                    </v-list-item>
                </v-list>

            </v-col>
        </v-row>

    </v-container>
</template>

<script>
    import $ from "jquery";

    export default {
        name: 'FormsView',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                formsUrl: 'http://localhost/ladiforms/',
                mediaUrl: 'http://localhost/storage/',
                forms: [],
            }
        },
        components: {
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.mediaUrl = `${this.$base_url}${process.env.VUE_APP_MEDIA_URL_PREFIX}`;
            this.formsUrl =  `${this.api_base_url}ladiforms/`;
            this.updateForms();
        },
        umounted() {},
        methods: {
            async updateForms() {
                $.ajax({
                    url: this.formsUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.forms = [];
                        response.forEach(form => {
                            // Required for logged superusers, otherwise they may be able to see also hidden content
                            if (form.public === 'True' || form.public === true) {
                                this.forms.push(form);
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

    .forms-list{
        border-radius: 2.5%;
        margin-top: 15px;
    }

</style>

