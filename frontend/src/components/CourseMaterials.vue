<template>
    <v-container fluid v-if="materials != null">

        <v-row v-if="materials.length !== 0" class="elevation-2 main-row"
               align="center" justify="center" >
            
            <v-col>

                <RefreshIcon icon="mdi-bookshelf" clickEvent="updateMaterials" />
                <v-spacer />

                <v-carousel hide-delimiters :progress="progressBarColor" :show-arrows="arrowsEnabled">

                    <template v-slot:prev="{ props }">
                        <v-btn variant="elevated"
                               :color="arrowsColor"
                               @click="props.onClick"
                               :icon="true"
                               id="button-left">
                            <v-icon size="x-large" color="white">
                                mdi-arrow-collapse-left
                            </v-icon>
                        </v-btn>
                    </template>
                    <template v-slot:next="{ props }">
                        <v-btn variant="elevated"
                               :color="arrowsColor"
                               @click="props.onClick"
                               :icon="true"
                               id="button-right" >
                            <v-icon size="x-large" color="white">
                                mdi-arrow-collapse-right
                            </v-icon>
                        </v-btn>
                    </template>

                    <!-- CSS scoped doesn't work properly here -->
                    <v-carousel-item v-for="(material, index) in materials" :key="`T${index}`" height="500"
                                     :style="{ 'padding-block': '15px', 'padding-inline': '15px' }">

                        <v-sheet height="100%" class="carousel-sheet"
                                 :style="{ 'padding-block': '20px', 'padding-inline': '7%',
                                            'border-radius': boxsBorderRadius }">

                            <v-container fluid>
                                <v-row align="center" justify="center">

                                    <CourseMaterialsCrumbs :crumbs="material.breadcrumbs" />

                                </v-row>
                                <v-row align="center" justify="center">

                                    <v-table fixed-header class="material-table">
                                        <thead>
                                            <tr v-if="userLang === 'it'">
                                                <th class="text-left">
                                                    Nome file
                                                </th>
                                                <th class="text-left">
                                                    Data di modifica
                                                </th>
                                                <th class="text-left">
                                                    Dimensione (MB)
                                                </th>
                                            </tr>
                                            <tr v-else>
                                                <th class="text-left">
                                                    Filename
                                                </th>
                                                <th class="text-left">
                                                    Modifications Date
                                                </th>
                                                <th class="text-left">
                                                    Size (MB)
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody v-if="material.files.length !== 0">
                                            <tr v-for="(file, index) in material.files" :key="`F${index}`">
                                                <td>
                                                    <a  class="site-anchor"
                                                        :href="file.url" target="_blank">
                                                        {{ file.name }}
                                                    </a>
                                                </td>
                                                <td>
                                                    <p>
                                                        {{ file.date }}
                                                    </p>
                                                </td>
                                                <td>
                                                    <p>
                                                        {{ file.size }}
                                                    </p>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </v-table>

                                </v-row>
                            </v-container>

                        </v-sheet>
                    </v-carousel-item>

                </v-carousel>

            </v-col>
        </v-row>

    </v-container>
</template>

<script>

    import CourseMaterialsCrumbs from '@/components/CourseMaterialsCrumbs.vue';
    import RefreshIcon from '@/components/RefreshIcon.vue';

    export default {
        name: 'CourseInfos',
        components: {
            CourseMaterialsCrumbs,
            RefreshIcon,
        },
        props: {
            'boxsBorderRadius': {
                type: String,
                default: function () {
                    return '15px';
                }
            },
            'progressBarColor': {
                type: String,
                default: function () {
                    return '#003576';
                }
            },
            'arrowsColor': {
                type: String,
                default: function () {
                    return '#003576';
                }
            },
            'materials': {
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
            arrowsEnabled: true,
        }),
        created(){
            this.emitter.on('updateMaterials', () => {
                this.updateMaterials();
            });
        },
        mounted() {
            this.arrowsEnabled = !this.isTouchDevice();
        },
        methods: {
            updateMaterials() {
                this.emitter.emit('updateMaterial');
                this.emitter.emit('updateMaterialCrumbs');
            },
            isTouchDevice() {
                return ('ontouchstart' in window) ||
                    (navigator.maxTouchPoints > 0) ||
                    (navigator.msMaxTouchPoints > 0);
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    #button-right {
        margin-right: 15px;
    }

    #button-left {
        margin-left: 15px;
    }

    #carousel-sheet {
        padding-block: 20px;
        padding-inline: 7%;
        border-radius: 15px;
    }

    .material-table{
        width: 100%;
        height: 320px;
        overflow-y: scroll;
    }

    v-carousel-item {
        padding: 15px;
    }

</style>