<template>
    <v-container>
        <v-row justify="center" align="center"
               class="elevation-4 main-row">
            <!-- Staff -->
            <v-col>
                <v-row justify="center" align="center">
                    <v-col md="1">
                        <RefreshIcon icon="mdi-account-group-outline" clickEvent="updateStaffs" />
                    </v-col>
                    <v-col>
                        <h3 id="staff-title" >LADI staff</h3>
                    </v-col>
                </v-row>
                <v-row justify="center" align="center">
                    <!-- Standard div with flex properties, waiting for v-flex implementation on vuetify 3 -->
                    <div class="flex-div">

                        <StaffCard  v-for="item in staffs" :key="item.id"
                                    :staff="item" :userLang="userLang" />

                    </div>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

    import StaffCard from '@/components/StaffCard.vue';
    import RefreshIcon from '@/components/RefreshIcon.vue';
    import $ from "jquery";

    export default {
        name: 'LADIStaff',
        data: function () {
            return {
                api_base_url: 'http://localhost/',
                staffsUrl: 'http://localhost/ladistaffs/',
                userUrl: 'http://localhost/ladiuser/?id=',
                staffs: [],
            }
        },
        props: {
            'userLang': {
                type: String,
                default: function () {
                    return 'it';
                }
            },
        },
        components: {
            StaffCard,
            RefreshIcon,
        },
        created(){
            this.emitter.on('updateStaffs', () => {
                this.updateStaffs();
            });
        },
        mounted() {
            this.api_base_url = this.$api_base_url;
            this.staffsUrl = `${this.api_base_url}ladistaffs/`;
            this.userUrl = `${this.api_base_url}ladiuser/?id=`
            this.updateStaffs();
        },
        methods: {
            async updateStaffs() {
                $.ajax({
                    url: this.staffsUrl,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        this.staffs = []
                        response.forEach((item) => this.updateUser(item));
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        console.error(textStatus, errorThrown);
                    }
                });
            },
            async updateUser(staff) {
                $.ajax({
                    url: this.userUrl + staff.user_id,
                    type: "get",
                    dataType: "json",
                    success: (response) => {
                        staff.fullname = `${response.name} ${response.surname}`;
                        staff.email = response.email;
                        this.staffs.push(staff);
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

    .staff-title {
        text-align: left;
        padding-top: 5px;
    }

    #staff-icon {
        padding-left: 50%;
    }

</style>
