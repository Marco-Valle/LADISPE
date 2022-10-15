<template>

    <div class="tooltip">  
        <v-icon size="x-large" @click="clickEventHandler()">
            {{ icon }}
        </v-icon>
        <span   v-if="userLang === 'it' && !isTouchDevice()"
                class="tooltiptext">
                clicca per ricaricare
        </span>
        <span v-else-if="!isTouchDevice()" class="tooltiptext">
                click to refresh
        </span>
    </div>

</template>

<script>

    export default {
        name: 'LADIContacts',
        data: function () {
            return {}
        },
        props: {
            'icon': {
                type: String,
                default: function () {
                    return 'mdi-refresh';
                }
            },
            'clickEvent': {
                type: String,
                default: function () {
                    return null;
                }
            },
            'userLang': {
                type: String,
                default: function () {
                    return 'it';
                }
            },
        },
        methods: {
            clickEventHandler () {
                if (this.clickEvent !== null){
                    this.emitter.emit(this.clickEvent);
                }
            },
            isTouchDevice() {
                return ('ontouchstart' in window) ||
                    (navigator.maxTouchPoints > 0) ||
                    (navigator.msMaxTouchPoints > 0);
            },
        }
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";
    @import "@/styles/tooltip.css";

</style>
