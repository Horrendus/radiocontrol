<!--
This file is part of radiocontrol.

Copyright (C) 2019 Stefan Derkits <stefan@derkits.at>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

<template>
    <div :style="playlistClass">
        <b>{{playlist.name}}</b>
        <br>
        {{convertTime(playlist.length)}}
    </div>
</template>

<script>
    export default {
        name: "Playlist",
        props: {
            playlist: Object
        },
        methods: {
            convertTime(sec) {
                    sec = Math.floor( sec );
                    let hours = Math.floor(sec / 3600);
                    (hours >= 1) ? sec = sec - (hours * 3600) : hours = '00';
                    let min = Math.floor(sec / 60);
                    (min >= 1) ? sec = sec - (min * 60) : min = '00';
                    (sec < 1) ? sec = '00' : void 0;

                    (min.toString().length == 1) ? min = '0' + min : void 0;
                    (sec.toString().length == 1) ? sec = '0' + sec : void 0;
                    return hours+':'+min+':'+sec;
                }
        },
        data() {
            return {
                playlistClass: {
                    border: "1px solid",
                    margin: "5px",
                    height: (this.playlist.length / 50) + "px"
                }
            }
        }
    }
</script>

<style scoped>

</style>