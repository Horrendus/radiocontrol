<template>
    <div class="Upload">
        Upload Playlists
        <form>
          <div>
            <label>Select file to upload</label>
            <input type="file" @change="onFileSelected">
          </div>
          <button @click="uploadFile">Upload Playlist</button>
        </form>
    </div>
</template>

<script>
    export default {
        name: "Upload",
        data() {
            return {
                file: null
            }
        },
        methods: {
            onFileSelected(event) {
                this.file = event.target.files[0]
            },
            async uploadFile() {
                const formData = new FormData();
                formData.append('playlist', this.file);

                try {
                  const response = await  fetch('http://localhost/playlists/', {
                    method: 'POST',
                    body: formData
                  });
                  const result = await response;
                  console.log('Success:', result.text());
                } catch (error) {
                  console.error('Error:', error);
                }
            }
        }
    }
</script>

<style scoped>

</style>