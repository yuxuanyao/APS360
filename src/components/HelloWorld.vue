<template>
    <div>
      <div class='uploadWrapper'>
        {{ msg }}
      </div>
      <div>
        <input type="file" accept="image/*" @change="encodeImageFileAsURL($event)" />
      </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "Upload an image of your face and we'll return a playlist for your mood.",
    };
  },
  methods: {
    encodeImageFileAsURL(element) {
      var file = element.target.files[0];
      var reader = new FileReader();
      reader.onloadend = function() {
        console.log('RESULT', reader.result)
      }
      reader.readAsDataURL(file);
    },
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.uploadWrapper {
  padding: 50px;
}
</style>
