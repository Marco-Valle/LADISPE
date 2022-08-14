<template>
    <v-container fluid class="border border-dark view-container" >

        <v-row>
            <!-- Optional gallery -->
            <Gallery class="home-box"
                     redirectOnClick="#newsTable"
                     galleryTitle="Home" />
        </v-row>

        <v-spacer />

        <v-row>
            <!-- News in evidence -->
            <InEvidenceNews class="home-box"
                            :truncateAfterNChars="70" />
        </v-row>

        <v-spacer />

        <v-row>
            <!-- News table -->
            <NewsTable class="home-box news-table" />
        </v-row>

    </v-container>
</template>

<script>
    import NewsTable from '@/components/NewsTable.vue';
    import Gallery from '@/components/Gallery.vue';
    import InEvidenceNews from '@/components/InEvidenceNews.vue';

    export default {
        name: 'HomeView',
        data: function () {
            return {}
        },
        components: {
            NewsTable,
            Gallery,
            InEvidenceNews,
        },
        mounted() {},
        methods: {}
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .home-box {
        margin-top: 15px;
    }

    .news-table {
        max-width: 1100px;
    }

</style>