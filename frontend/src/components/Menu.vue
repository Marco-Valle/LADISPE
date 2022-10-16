<template>
    <v-container fluid class="border border-dark menu-box" >
        
        <v-row v-for="item in menu" :key="item.text" justify="center">
            <v-col class="menu-column">
                
                <v-btn  elevation="5" outlined class="my-button"
                        :to=item.to @click="openUrl(item.staticUrl)">
                    <h4 v-if="userLang === 'it'">
                        <v-icon v-if="item.icon !== ''"
                                size="large" class="menu-icon" >
                            {{ item.icon }}
                        </v-icon>
                        {{ item.textIT }}
                    </h4>
                    <h4 v-else>
                        <v-icon v-if="item.icon !== ''"
                                size="large" class="menu-icon" >
                            {{ item.icon }}
                        </v-icon>
                        {{ item.text }}
                    </h4>
                </v-btn>

            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col class="menu-column">
                
                <v-btn  elevation="5" outlined class="my-button"
                        @click="updateLang()">
                        <v-icon size="large" class="menu-icon">
                            mdi-translate
                        </v-icon>
                </v-btn>

            </v-col>
        </v-row>

    </v-container>
</template>

<script>

    export default {
        name: 'LADIMenu',
        data: function () {
            return {
                userLang: this.$settings.userLang,
            }
        },
        props: {
            'menu': {
                type: Array,
                default: function () {
                    return [];
                }
            },
        },
        methods: {
            updateLang() {
                const newUserLang = (this.userLang == 'en') ? 'it' : 'en';
                this.emitter.emit('updateLang', { 'lang': newUserLang });
                this.userLang = newUserLang;
                this.$settings.userLang = newUserLang;
            },
            openUrl(url) {
                if (url === '') { return; }
                window.open(url).focus();
            },
        }
    }
</script>

<style scoped>

    @import "@/styles/main.css";

    .menu-box {
        border-radius: 15px;
        background-color: #eeeeee;
    }

    .menu-column {
        width: 100%;
        padding-inline: 20%
    }

    .menu-icon {
        margin-right: 4px;
    }

    h4 {
        color: white;
        text-align: center;
    }

</style>
