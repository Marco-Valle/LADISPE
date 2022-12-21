<template>
    <!-- Desktop header -->
    <v-container fluid>
        
        <v-row justify="center" class="header-upper-row">
        </v-row>

        <v-row class="header-row">
            <v-col cols="3" offset="1">
                <a  class="site-anchor"
                    href="https://www.polito.it">
                    <v-img alt="POLITO LOGO" :src="logo" height="107" width="243" />
                </a>
            </v-col>
            <v-col offset="1">
                <h1 class="header-title">LADISPE</h1>
                <h2 class="header-title">Dipartimento di Automatica e Informatica</h2>
            </v-col>
            <v-col cols="1"><v-spacer /></v-col>
        </v-row>

        <v-row justify="center" class="header-bottom-row">
        </v-row>

    </v-container>
</template>

<script>
    import logo from '@/assets/logo_poli.svg';

    export default {
        name: 'LADIHeader',
        components: {},
        props: {},
        data: () => ({
            logo: logo,
        }),
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .header-bottom-row {
        background-color: #007baa;
        height: 5px;
        margin-top: 5px;
    }

    .header-upper-row {
        background-color: #003576;
        height: 30px;
    }

    .header-row {
        margin-top: 1px;
        background-color: white;
    }

    .header-title {
        color: #003576;
        text-align: right;
    }

</style>