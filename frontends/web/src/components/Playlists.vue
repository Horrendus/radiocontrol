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
    <div>
        <h1>Playlists</h1>
        <ul>
            <li v-for="playlist in playlists"
                :key="playlist.name">{{playlist.name}} : {{playlist.status}} - {{playlist.length}}</li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "Playlists",
        data: function () {
            return {
                playlists: []
            }
        },
        methods: {
            async fetchPlaylists(endpoint) {
                const res = await fetch(endpoint);
                const playlists = await res.json();

                return playlists;
            },
        },
        mounted() {
            this.fetchPlaylists('http://localhost/playlists').then(playlists => {this.playlists = playlists})
        }
    }
</script>

<style scoped>

</style>
