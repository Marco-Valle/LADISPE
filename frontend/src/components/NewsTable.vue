<template>
    <v-container fluid>
        <v-row justify="center" align="center" class="elevation-2 main-row" >
            <!-- News table -->
            <v-col cols="12">
                <v-card elevation="2"
                        class="border border-dark news-card" >

                    <v-card-title>
                        <v-container fluid>
                            <v-row justify="center" align="center">
                                <v-col cols="1">
                                    <div :class="tableHeader.loadingDivClass" >
                                        <refresh @click="defaultTableUpdate"
                                                 :size="38" />
                                    </div>
                                </v-col>
                                <v-col cols="1" sm="2" md="4" lg="6" xl="6" xxl="6" >
                                    <h3 v-if="isLargeScreen">LADI news</h3>
                                    <v-spacer />
                                </v-col>
                                <v-col cols="9" sm="9" md="7" lg="5" xl="5" xxl="5">
                                    <v-text-field v-model="tableHeader.searchedText"
                                                  @change="defaultTableUpdate"
                                                  @click:clear="defaultTableUpdate"
                                                  append-icon="mdi-magnify"
                                                  label="Search"
                                                  single-line
                                                  clearable
                                                  hide-details />
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-title>
                    <p id="newsTable" /> <!-- Just an anchor for the table -->
                    <v-container class="table-container" :style="{'max-width': maxTableWidth}">
                        <v-row align="center" justify="center">
                            <v-col>
                                <TableLite :is-loading="table.isLoading"
                                    :columns="table.columns"
                                    :rows="table.rows"
                                    :total="table.totalRecordCount"
                                    :sortable="table.sortable"
                                    :messages="table.messages"
                                    @do-search="updateTable"
                                    @is-finished="table.isLoading = false" />
                            </v-col>
                        </v-row>
                    </v-container>
                    
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import TableLite from "vue3-table-lite";
    import refresh from 'vue-material-design-icons/Refresh.vue';
    import $ from "jquery";
    import { computed } from "vue";
    import { useDisplay } from "vuetify";

    export default {
        name: 'NewsTable',
        components: {
            TableLite,
            refresh
        },
        props: {
            'menu': {
                type: Array,
                default: function () {
                    return [];
                }
            },
            'externalSearchedText': {
                type: String,
                default: function () {
                    return '';
                }
            },
        },
        data: () => ({
            longestNewsChars: 0,
            api_base_url: 'http://localhost/',
            newsUrl: 'http://localhost/ladinews/',
            tableHeader: {
                'searchedText': '',
                'loadingDivClass': 'loading-div icon-div',
            },
            table: {
                isLoading: false,
                columns: [
                    {
                        label: navigator.language || navigator.userLanguage === 'it' ? 'Titolo' : 'Title',
                        field: "title",
                        width: "20%",
                        sortable: true,
                        isKey: true,
                        display: function (row) {
                            return (
                                '<h4 id="newsTable-' + row.id + '" align="center">' +
                                '<a class="site-anchor" href = "'+ row.link +'" data - id="' + row.id +
                                '" style="text-decoration: none; color: #003576";>' +
                                row.title +
                                "</a></h4>"
                            );
                        }
                    },
                    {
                        label: navigator.language || navigator.userLanguage === 'it' ? 'Data' : 'Date',
                        field: "timestamp",
                        width: "20%",
                        sortable: true,
                        display: function (row) {
                            return (
                                '<p align="center">' + row.timestamp.split('T')[0] + '</p>'
                            );
                        }
                    },
                    {
                        label: navigator.language || navigator.userLanguage === 'it' ? 'Testo' : 'Text',
                        field: "text",
                        width: "60%",
                        sortable: false,
                        display: function (row) {
                            return (
                                '<p align="center" style="/*white-space: pre;*/  overflow-wrap: break-word; ">' + row.text + '</p>'
                            );
                        }
                    }
                ],
                rows: [],
                totalRecordCount: 1,
                sortable: {
                    order: "timestamp",
                    sort: "desc",
                }
            }
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
        created() {
            this.emitter.on('newsSearch', (evt) => {
                this.externalSearchById(evt.id);
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.newsUrl = `${this.api_base_url}ladinews/`;
            this.defaultTableUpdate();
        },
        unmounted() {},
        computed: {
            isTableLoading() {
                return this.table.isLoading;
            },
            maxTableWidth() {
                if (this.longestNewsChars < 10){
                    return '550px';
                } else if (this.longestNewsChars < 40) {
                    return '650px';
                } else if (this.longestNewsChars < 70) {
                    return '850px';
                } else {
                    return '900px';
                }
            }
        },
        watch: {
            isTableLoading() {
                this.tableHeader.loadingDivClass = this.table.isLoading ? 'loading-div icon-div' : 'icon-div';
            }
        },
        methods: {
            defaultTableUpdate() {
                this.updateTable(0, 10, this.table.sortable.order, this.table.sortable.sort);
            },
            async updateTotalRecordCount(keyword) {
                const tableWasLoading = this.table.isLoading;
                const tmpUrl = `count/?keyword=${ keyword }`;
                console.log(keyword);
                if (!tableWasLoading) { this.table.isLoading = true; }
                $.ajax({
                    url: this.newsUrl + tmpUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.table.totalRecordCount = response;
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        this.table.totalRecordCount = 0;
                        console.error(textStatus, errorThrown);
                    },
                    complete: () => {
                        if (!tableWasLoading) { this.table.isLoading = false; }
                    },
                });
            },
            async updateTable(offset, limit, order, sort) {
                this.table.isLoading = true;
                this.table.sortable.order = order;
                this.table.sortable.sort = sort;
                // If the search field is empty search all
                const keyword = this.tableHeader.searchedText !== '' && this.tableHeader.searchedText != null ? this.tableHeader.searchedText : '*';
                const tmpUrl = `?keyword=${ keyword }&offset=${ offset }&limit=${ limit }&order=${ order }&sort=${ sort }`;
                $.ajax({
                    url: this.newsUrl + tmpUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.updateTotalRecordCount(keyword);
                        this.table.rows = [];
                        this.longestNewsChars = 0;
                        response.forEach(row => {
                            if (row.link === null) { row.link = '#newsTable' }
                            if (row.text.length > this.longestNewsChars){ 
                                this.longestNewsChars = row.text.length;
                            }
                            this.table.rows.push(row);
                        });
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        this.table.totalRecordCount = 0;
                        console.error(textStatus, errorThrown);
                    },
                    complete: () => {
                        this.table.isLoading = false;
                    },
                });
            },
            async externalSearchById(id) {

                if (id <= 0) {
                    this.tableHeader.searchedText = '';
                    this.defaultTableUpdate();
                    return;
                }
                $.ajax({
                    url: this.newsUrl + '?id=' + id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.tableHeader.searchedText = response.title
                        this.defaultTableUpdate();
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
        }
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

    .icon-div {
        color: #003576;
        display: inline-block;
        float: none;
        padding-left: 2px;
        padding-top: 7px;
    }
    
    .loading-div {
        animation-name: spin;
        animation-duration: 2000ms;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }

    .news-card {
        background-color: white;
        border-radius: 15px;
    }

    .table-container {
        max-width: 700px; // default value (overrided by JS)
        padding-top: 5px;
    }

    h4 {
        color: white;
    }

    @keyframes spin {
        from {
            transform: rotate(0deg);
        }

        to {
            transform: rotate(360deg);
        }
    }

    ::v-deep(.vtl-table .vtl-thead .vtl-thead-th) {
        color: #fff;
        background-color: #003576;
        border-color: #486293;
    }

    ::v-deep(.vtl-table td),
    ::v-deep(.vtl-table tr) {
        border: none;
    }

    ::v-deep(.vtl-paging-info) {
        color: #486293;
    }

    ::v-deep(.vtl-paging-count-label),
    ::v-deep(.vtl-paging-page-label) {
        color: #486293;
    }

    ::v-deep(.vtl-paging-pagination-page-link) {
        border: none;
    }

</style>
