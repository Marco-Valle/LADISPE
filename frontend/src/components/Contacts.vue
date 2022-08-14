<template>
    <v-container fluid>

        <v-row justify="center" align="center" class="elevation-4 main-row" >

            <v-col>
                <v-row class="time-row"
                       justify="center" align="center" >

                    <!-- Orari -->

                    <v-col v-if="userLang === 'it'" class="timetable">
                        <h3>
                            <v-icon size="large">
                                mdi-clock-outline
                            </v-icon>
                            Orari
                        </h3>
                        <p>
                            Il LADISPE &egrave; aperto dal luned&igrave; al venerd&igrave; dalle 8:30 alle 18:30.<br />
                            Per attivit&agrave; estranee alle esercitazioni registrate &egrave; necessario concordare preventivamente con il personale l'uso delle risorse.<br />
                            Dopo le 18:30 l'accesso &egrave; consentito solo ai corsi autorizzati e sotto la responsabilit&aacute; dell'esercitatore.
                        </p>
                    </v-col>

                    <v-col v-else class="timetable">
                        <h3>
                            <v-icon size="large">
                                mdi-clock-outline
                            </v-icon>
                            Opening times
                        </h3>
                        <p>
                            LADISPE is open from Monday to Friday from 8:30 to 18:30.<br />
                            A reservation is requied for any activity, excluded the scheduled exercitations.<br />
                            After the 18:30 the acces is allowed just for the authorized courses and under the trainer's responsability.
                        </p>
                    </v-col>

                </v-row>
                <v-row justify="center" align="center">

                    <!-- Indirizzo, telefono, fax & email  -->

                    <v-col class="contacts-infos">
                        <h3 v-if="userLang === 'it'">
                            <v-icon @click="openMap(7.662360, 45.062450, 'LADISPE+POLITO')"
                                    size="large">
                                mdi-map-outline
                            </v-icon>
                            Indirizzo
                        </h3>
                        <h3 v-else>
                            <v-icon @click="openMap(7.662360, 45.062450, 'LADISPE+POLITO')"
                                    size="large">
                                mdi-map-outline
                            </v-icon>
                            Address
                        </h3>
                        <p class="info-paragraph">
                            <a href="geo:7.662360,45.062450?q=LADISPE+POLITO">
                                Laboratorio LADISPE <br />
                                C/O DAUIN - Politecnico di Torino <br />
                                Corso Duca degli Abruzzi 24 <br />
                                10129 Torino (TO), Italy <br />
                            </a>
                        </p>
                    </v-col>

                    <v-col class="contacts-infos">
                        <h3 v-if="userLang === 'it'" >
                            <v-icon @click="call('00390110907045')"
                                    size="large">
                                mdi-phone-outline
                            </v-icon>
                            Telefono e fax
                        </h3>
                        <h3 v-else>
                            <v-icon @click="call('00390110907045')"
                                    size="large">
                                mdi-phone-outline
                            </v-icon>
                            Phone and Fax
                        </h3>
                        <p class="info-paragraph">
                            <a href="tel:00390110907045">Tel: (+39) 011 090 7045</a><br />
                            Fax: (+39) 011 090 7099

                        </p>
                    </v-col>

                    <v-col class="contacts-infos">
                        <h3>
                            <v-icon @click="email('ladispe@polito.it')"
                                    size="large">
                                mdi-email-outline
                            </v-icon>
                            Email
                        </h3>
                        <p class="info-paragraph">
                            <a href="mailto:ladispe@polito.it">
                                ladispe@polito.it
                            </a>
                        </p>
                    </v-col>

                </v-row>
            </v-col>

        </v-row>

    </v-container>
</template>

<script>

    export default {
        name: 'LADIContacts',
        data: function () {
            return {
                userLang: navigator.language || navigator.userLanguage,
            }
        },
        props: {},
        methods: {
            call(phoneN) {
                window.open('tel:' + phoneN, '_self');
            },
            email(email) {
                window.open('mailto:' + email, '_self');
            },
            openMap(longitude, latitude, keyword) {
                window.open(`geo:${longitude},${latitude}?q=${keyword}`, '_self');
            },
        }
    }
</script>

<style lang="scss" scoped>

    @import "@/styles/main.css";

    .contacts-infos > h3 {
        text-align: center;
        margin-bottom: 5px;
    }

    .info-paragraph{
        text-align: center;
    }

    .timetable > h3 {
        margin-bottom: 10px;
    }

    .time-row {
        margin-bottom: 15px;
    }

</style>
