<template>
  <div class="home">
    <Playlists></Playlists>
  </div>
</template>

<script>
// @ is an alias to /src
import Playlists from "@/components/Playlists.vue"

export default {
  name: 'home',
  components: {
    Playlists
  }
}
</script>
