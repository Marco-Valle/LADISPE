<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row>
            <!-- Orari, telefono, fax, email & indirizzo-->
            <Contacts :userLang="userLang" />
        </v-row>

        <v-row>
            <!-- Staff -->
            <Staff :userLang="userLang" />
        </v-row>

</v-container>
</template>

<script>
    import Contacts from '@/components/Contacts.vue';
    import Staff from '@/components/Staff.vue';

    export default {
        name: 'ContactsView',
        data: function () {
            return {
                userLang: this.$settings.userLang,
            }
        },
        created() {
            this.emitter.on('updateLang', (evt) => {
                this.userLang = evt.lang;
            });
        },
        components: {
            Contacts,
            Staff,
        },
    }

</script>

<style scoped>

    @import "@/styles/main.css";

</style>