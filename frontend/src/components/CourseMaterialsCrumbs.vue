<template>
    <v-container fluid>

        <v-row align="center" justify="center">
            <v-col>

                <v-breadcrumbs :items="breadcrumbs">
                    <template v-slot:divider>
                         <v-icon icon="mdi-chevron-right"></v-icon>
                    </template>
                </v-breadcrumbs>

            </v-col>
        </v-row>

    </v-container>
</template>

<script>

    export default {
        name: 'CourseMaterialsCrumbs',
        components: {},
        props: {
            'crumbs': {
                type: Object,
                required: true
            },
        },
        data: () => ({
            breadcrumbs: [],
        }),
        created() {
            this.emitter.on('updateMaterialCrumbs', () => {
                this.prepareCrumbs();
            });
        },
        mounted() {
            this.prepareCrumbs();
        },
        methods: {
            prepareCrumbs() {
                this.breadcrumbs = [this.formatCrumb('Root')];
                this.crumbs.forEach( crumb => {
                    this.breadcrumbs.push(this.formatCrumb(crumb));
                });
            },
            formatCrumb(crumb) {
                const new_crumb = {
                    title: crumb,
                    disabled: false,
                    href: '',
                };
                return new_crumb;
            },
        }
    }
</script>