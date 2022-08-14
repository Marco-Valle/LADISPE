<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row>
            <!-- Orari, telefono, fax, email & indirizzo-->
            <Contacts />
        </v-row>

        <v-row>
            <!-- Staff -->
            <Staff />
        </v-row>

</v-container>
</template>

<script>
    import Contacts from '@/components/Contacts.vue';
    import Staff from '@/components/Staff.vue';

    export default {
        name: 'ContactsView',
        data: function () {
            return {}
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